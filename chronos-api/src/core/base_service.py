from motor.motor_asyncio import AsyncIOMotorDatabase

class BaseService:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.database = database
