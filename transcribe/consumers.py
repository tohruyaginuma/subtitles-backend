import asyncio
import json
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from accounts.models import User
from histories.models import History, HistorySet
from channels.db import database_sync_to_async
from datetime import datetime

TYPE_SYSTEM = {
    "SYSTEM": "system",
    "TRANSCRIPTION": "transcription",
    "ERROR": "error",
}

class WebSocketTranscriptHandler(TranscriptResultStreamHandler):
    def __init__(self, stream, websocket):
        super().__init__(stream)
        self.websocket = websocket

    async def handle_transcript_event(self, event: TranscriptEvent):
        for result in event.transcript.results:
            for alt in result.alternatives:
                await self.websocket.send(text_data=json.dumps({
                    "data": {
                        "type": TYPE_SYSTEM["TRANSCRIPTION"],
                        "content": alt.transcript,
                        "is_partial": result.is_partial,
                    },
                    "error": None
                }))

class TranscribeConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_queue = asyncio.Queue()
        self.transcribe_task = None
        self.transcribe_started = False
        self.user = None
        self.transcribe_set = None

    async def connect(self):
        await self.accept()
        
        await self.send(text_data=json.dumps({
            "data": {
                "type": TYPE_SYSTEM["SYSTEM"],
                "content": "🔊 Connected and ready for audio.",
            },
            "error": None
        }))

        # Start transcription only when audio begins
        if not self.transcribe_started:
            self.transcribe_task = asyncio.create_task(self.stream_to_transcribe())
            self.transcribe_started = True
            print("🚀 Transcribe task started")

        print("✅ WebSocket connected")

    async def disconnect(self, close_code):
        if self.transcribe_task:
            self.transcribe_task.cancel()
        print("🔌 WebSocket disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            print(f"📥 Received {len(bytes_data)} bytes")

            await self.audio_queue.put(bytes_data)

    async def stream_to_transcribe(self):
        print("🔁 stream_to_transcribe starting...")
        try:
            client = TranscribeStreamingClient(
                region=settings.AWS_REGION,
            )

            # Start stream (no audio_stream param)
            stream = await client.start_stream_transcription(
                language_code="en-US",
                media_sample_rate_hz=16000,
                media_encoding="pcm",
            )

            print("✅ AWS Transcribe stream started")

            async def send_audio():
                print("🎧 send_audio generator activated")
                try:
                    while True:
                        chunk = await self.audio_queue.get()
                        print(f"🎙️ Sending chunk to AWS Transcribe: {len(chunk)} bytes")
                        await stream.input_stream.send_audio_event(audio_chunk=chunk)
                except asyncio.CancelledError:
                    print("🛑 send_audio cancelled")
                    await stream.input_stream.end_stream()
                    raise

            async def receive_transcripts():
                handler = WebSocketTranscriptHandler(stream.output_stream, self)
                print("🔁 handler activated")
                try:
                    await handler.handle_events()
                except asyncio.CancelledError:
                    print("🛑 receive_transcripts cancelled")
                    raise
                except Exception as e:
                    print(f"❗ Transcript handling error: {e}")

            await asyncio.gather(
                asyncio.shield(send_audio()),
                asyncio.shield(receive_transcripts())
            )

        except Exception as e:
            print(f"❌ Error in stream_to_transcribe: {e}")
            await self.send(text_data=json.dumps({
                "data": None,
                "error": {
                    "type": TYPE_SYSTEM["ERROR"],
                    "content": str(e)
                }}
            ))