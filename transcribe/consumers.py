import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from accounts.models import User
from histories.models import Transcribe, TranscribeSet
from channels.db import database_sync_to_async
from datetime import datetime

class WebSocketTranscriptHandler(TranscriptResultStreamHandler):
    def __init__(self, stream, websocket):
        super().__init__(stream)
        self.websocket = websocket

    async def handle_transcript_event(self, event: TranscriptEvent):
        for result in event.transcript.results:
            for alt in result.alternatives:
                await self.websocket.send(text_data=json.dumps({
                    "type": "transcription",
                    "is_partial": result.is_partial,
                    "transcript": alt.transcript,
                }))

class TranscribeConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_queue = asyncio.Queue()
        self.transcribe_task = None
        self.transcribe_started = False
        self.user = None
        self.transcribe_set = None
    
    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_transcribe_set(self, transcribe_set_id):
        return TranscribeSet.objects.get(id=transcribe_set_id)

    @database_sync_to_async
    def create_transcribe_set(self, title):
        return TranscribeSet.objects.create(user_id=self.user, title=title)
    
    @database_sync_to_async
    def create_transcribe(self, sentence):
        return Transcribe.objects.create(sentence=sentence, user_id=self.user, transcribe_set_id=self.transcribe_set)

    async def connect(self):
        await self.accept()
        
        await self.send(text_data=json.dumps({
            "type": "system",
            "message": "🔊 Connected and ready for audio."
        }))
        print("✅ WebSocket connected")

    async def disconnect(self, close_code):
        if self.transcribe_task:
            self.transcribe_task.cancel()
        print("🔌 WebSocket disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            print(f"📥 Received {len(bytes_data)} bytes")

            # Start transcription only when audio begins
            if not self.transcribe_started:
                self.transcribe_task = asyncio.create_task(self.stream_to_transcribe())
                self.transcribe_started = True
                print("🚀 Transcribe task started")
            
            print("self.scope['user'].is_authenticated -----", self.scope['user'].is_authenticated)
            if self.scope['user'].is_authenticated:
                if not self.user:
                    user_id = self.scope['user'].id
                    self.user = await self.get_user(user_id)
                    print("✅ User set")

                if not self.transcribe_set:
                    title = f"Subtitle at {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    self.transcribe_set = await self.create_transcribe_set(title)
                    print("✅ Transcribe set created")

            await self.audio_queue.put(bytes_data)

    async def stream_to_transcribe(self):
        print("🔁 stream_to_transcribe starting...")
        try:
            client = TranscribeStreamingClient(region="us-west-2")

            # Start stream (no audio_stream param)
            stream = await client.start_stream_transcription(
                language_code="en-US",
                media_sample_rate_hz=16000,
                media_encoding="pcm",
            )

            print("✅ AWS Transcribe stream started")

            async def send_audio():
                print("🎧 send_audio generator activated")
                while True:
                    chunk = await self.audio_queue.get()
                    print(f"🎙️ Sending chunk to AWS Transcribe: {len(chunk)} bytes")
                    await stream.input_stream.send_audio_event(audio_chunk=chunk)

            async def receive_transcripts():
                handler = WebSocketTranscriptHandler(stream.output_stream, self)
                await handler.handle_events()

            await asyncio.gather(send_audio(), receive_transcripts())

        except Exception as e:
            print(f"❌ Error in stream_to_transcribe: {e}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": str(e)
            }))