import json

from src.core.base_service import BaseService
from src.message.message_repository import MessageRepository
from src.message.merchant_repository import MerchantRepository
from src.core.nats import NatsConnection


class MessageService(BaseService):
    def __init__(self, database, nats: NatsConnection):
        super().__init__(database)
        self.nats = nats

    async def ratify_message(self, msg_id: str):
        """Ratify a message: get data, mark in DB, save to merchant collection, and publish to NATS"""
        repository = MessageRepository(self.database)
        merchant_repo = MerchantRepository(self.database)
        
        # Get the full message data first
        message_data = await repository.get_by_id(msg_id)
        
        if not message_data:
            return {"error": "Message not found", "message_id": msg_id}
            
        merchant_id = message_data.get("merchantId")
        if not merchant_id:
             return {"error": "Message does not have a merchantId", "message_id": msg_id}
        
        # Mark as ratified in database
        await repository.mark_as_ratified(msg_id)
        
        # Save msgId to merchant's collection
        await merchant_repo.add_message(merchant_id, msg_id)
        
        # Update ratified status for NATS
        message_data["ratified"] = True
        
        # Publish full message data to NATS as string
        await self.nats.publish(
            "hermes.ratified.msg",
            json.dumps(message_data).encode()
        )
        
        return message_data

    async def get_unratified_messages(self):
        """Get all messages that have not been ratified"""
        repository = MessageRepository(self.database)
        return await repository.get_unratified()
