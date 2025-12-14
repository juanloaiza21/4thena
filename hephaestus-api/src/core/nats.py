from nats.aio.client import Client as NATS

from src.core.config import settings
from src.core.core_deps import logger


class NatsConnection:
    """NATS connection for publishing messages only"""
    
    def __init__(self) -> None:
        self.NATS_URI = settings.NATS_URI
        self._client: NATS = None

    async def _create_connection(self) -> NATS:
        self._client = NATS()

        try:
            await self._client.connect(
                servers=[self.NATS_URI],
                name="hephaestus-client",
            )
            logger.info("NATS client connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            raise

        return self._client

    async def get_connection(self) -> NATS:
        if self._client is None or not self._client.is_connected:
            await self._create_connection()
        return self._client

    async def publish(self, subject: str, data: bytes) -> None:
        """Publish a message to a NATS subject"""
        if self._client is None or not self._client.is_connected:
            await self._create_connection()

        await self._client.publish(subject, data)
        logger.info(f"Published message to {subject}")

    async def close(self):
        if self._client is not None and self._client.is_connected:
            await self._client.close()
            logger.info("NATS connection closed")
