from typing import Callable, List
from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig

from src.core.config import settings
from src.core.core_deps import logger


class NatsConnection:
    def __init__(self, subjects: str | List[str], on_message: Callable) -> None:
        self.NATS_URI = settings.NATS_URI
        self.subjects = subjects if isinstance(subjects, list) else [subjects]
        self._on_message = on_message
        self._client: NATS = None
        self._subscriptions = []

    async def _on_connect(self) -> None:
        logger.info(f"Connected to NATS. Subscribing to subjects: {self.subjects}")

        for subject in self.subjects:
            sub = await self._client.subscribe(subject, cb=self._message_handler)
            self._subscriptions.append(sub)
            logger.info(f"Subscribed to subject: {subject}")

    async def _message_handler(self, msg):
        """Internal message handler that wraps the user's callback"""
        logger.info(f"Received message on {msg.subject}: {msg.data.decode()}")
        await self._on_message(msg)

    async def _create_connection(self) -> NATS:
        self._client = NATS()

        try:
            await self._client.connect(
                servers=[self.NATS_URI],
                name=settings.NATS_CLIENT_NAME
                if hasattr(settings, "NATS_CLIENT_NAME")
                else "chronos-client",
            )
            logger.info("NATS client connected successfully")
            await self._on_connect()
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            raise

        return self._client

    async def get_connection(self) -> NATS:
        if self._client is None or not self._client.is_connected:
            await self._create_connection()
        return self._client

    async def publish(self, subject: str, data: bytes) -> None:
        """
        Publish a message to a NATS subject
        """
        if self._client is None or not self._client.is_connected:
            await self._create_connection()

        await self._client.publish(subject, data)
        logger.info(f"Published message to {subject}")

    async def close(self):
        if self._client is not None and self._client.is_connected:
            for sub in self._subscriptions:
                await sub.unsubscribe()

            await self._client.close()
            logger.info("NATS connection closed")
