from bson import ObjectId

from src.core.base_repository import BaseRepository
from src.message.message_dto import RatifyMessageDto
from src.message.message_model import Message


class MessageRepository(BaseRepository[Message, RatifyMessageDto]):
    def __init__(self, database):
        collection = database["messages"]
        super().__init__(collection)

    async def get_unratified(self):
        """Get all messages that have not been ratified"""
        cursor = self.collection.find({
            "ratified": {"$ne": True},
            "merchant_id": {"$exists": True, "$nin": [None, ""]}
        })
        documents = await cursor.to_list(length=None)
        return [self._document_to_standard_dict(doc) for doc in documents]

    async def get_by_id(self, msg_id: str):
        """Get a message by its ID"""
        doc = await self.collection.find_one({"_id": ObjectId(msg_id)})
        return self._document_to_standard_dict(doc)

    async def mark_as_ratified(self, msg_id: str, merchant_id: str):
        """Mark a message as ratified and update merchant_id"""
        result = await self.collection.update_one(
            {"_id": ObjectId(msg_id)},
            {"$set": {"ratified": True, "merchant_id": merchant_id}}
        )
        return result.modified_count > 0
