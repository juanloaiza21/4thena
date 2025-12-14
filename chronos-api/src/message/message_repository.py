from src.core.base_repository import BaseRepository
from src.message.message_dto import CreateMessageDto
from src.message.message_model import Message


class MessageRepository(BaseRepository[Message, CreateMessageDto]):
    def __init__(self, database):
        collection = database["messages"]
        super().__init__(collection)
