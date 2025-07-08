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
        await self.send(text_data="🔊 Connected...")

    async def disconnect(self, close_code):
        await self.send(text_data="🔊 Disconnected...")
        pass

    async def receive(self, bytes_data=None):
        print(f"Received {len(bytes_data)} bytes")
        # Handle the binary audio data here
        # For example, forward this to an async generator or AWS Transcribe
        await self.send(text_data=f"Received {len(bytes_data)} bytes")