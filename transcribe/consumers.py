import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import aiofile
import boto3
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

boto3.setup_default_session(profile_name="t.yaginuma")

class WebSocketTranscriptHandler(TranscriptResultStreamHandler):
    def __init__(self, stream, websocket):
        super().__init__(stream)
        self.websocket = websocket

    async def handle_transcript_event(self, event: TranscriptEvent):
        for result in event.transcript.results:
            for alt in result.alternatives:
                await self.websocket.send(text_data=alt.transcript)

class TranscribeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # await self.send(text_data="🔊 Starting transcription...")

        file_path = "kei.pcm"
        client = TranscribeStreamingClient(region="us-west-2")

        stream = await client.start_stream_transcription(
            language_code="en-US",
            media_sample_rate_hz=16000,
            media_encoding="pcm"
        )

        handler = WebSocketTranscriptHandler(stream.output_stream, self)

        async def send_audio():
            async with aiofile.AIOFile(file_path, 'rb') as afp:
                reader = aiofile.Reader(afp, chunk_size=1024 * 16)
                async for chunk in reader:
                    await stream.input_stream.send_audio_event(audio_chunk=chunk)
            await stream.input_stream.end_stream()

        await asyncio.gather(send_audio(), handler.handle_events())
        await self.send(text_data="✅ Transcription complete.")
        await self.close()

    def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=f"You said: {text_data}")
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        # self.send(text_data=json.dumps({"message": message}))