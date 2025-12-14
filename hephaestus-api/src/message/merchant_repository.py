from motor.motor_asyncio import AsyncIOMotorDatabase


class MerchantRepository:
    """Repository for storing merchant-message relationships"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database

    def _get_collection(self, merchant_id: str):
        """Get or create a collection named after the merchantId"""
        return self.database[merchant_id]

    async def add_message(self, merchant_id: str, msg_id: str):
        """Add a message ID to the merchant's collection"""
        collection = self._get_collection(merchant_id)
        result = await collection.insert_one({"msg_id": msg_id})
        return str(result.inserted_id)

    async def get_messages(self, merchant_id: str):
        """Get all message IDs for a merchant"""
        collection = self._get_collection(merchant_id)
        cursor = collection.find({})
        documents = await cursor.to_list(length=None)
        return [doc["msg_id"] for doc in documents]
