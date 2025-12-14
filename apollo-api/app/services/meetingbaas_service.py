import httpx
from app.core.config import settings

MEETING_BAAS_BASE_URL = "https://api.meetingbaas.com/v2"

class MeetingBaasService:
    def __init__(self):
        self.api_key = settings.MEETING_BAAS_API_KEY
        self.headers = {
            "x-meeting-baas-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    async def join_meet(self, meeting_url: str, bot_name: str = "Apollo Recorder", webhook_url: str | None = None):
        """
        Send a bot to join a Google Meet and record it.
        """
        payload = {
            "meeting_url": meeting_url,
            "bot_name": bot_name,
            "reserved": False,
            "recording_mode": "speaker_view",
            "bot_image": "https://meetingbaas.com/static/972c82ad9de545ed803e3e2a8b5c8785/630fb/meeting-baas-fish.webp",
            "entry_message": "Apollo Recorder has joined. This meeting will be recorded.",
            "deduplication_key": meeting_url,
        }
        
        if webhook_url:
            payload["webhook_url"] = webhook_url

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MEETING_BAAS_BASE_URL}/bots",
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def get_bot(self, bot_id: str):
        """
        Get status of a specific bot.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{MEETING_BAAS_BASE_URL}/bots/{bot_id}",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def list_bots(self):
        """
        List all bots.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{MEETING_BAAS_BASE_URL}/bots",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def delete_bot(self, bot_id: str):
        """
        Remove a bot from a meeting.
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{MEETING_BAAS_BASE_URL}/bots/{bot_id}",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return {"status": "deleted"}

meetingbaas_service = MeetingBaasService()
