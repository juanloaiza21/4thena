import json

from src.core.base_service import BaseService
from src.message.message_repository import MessageRepository
from src.message.message_model import Message
from src.core.nats import NatsConnection


class MessageService(BaseService):
    def __init__(self, database, nats: NatsConnection):
        super().__init__(database)
        self.nats = nats

    async def create_message(self, body):
        repository = MessageRepository(self.database)
        message = await repository.create(body)
        await self.nats.publish(
            "hera.new.msgs",
            json.dumps(message).encode()
        )
        return message

    def get_all_messages(self):
        repository = MessageRepository(Message, self.database)
        return repository.get_all()
