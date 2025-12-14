from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi_router_controller import Controller

from src.deps import get_db, get_nats
from src.message.message_service import MessageService
from src.message.message_dto import CreateMessageDto
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.nats import NatsConnection

router = APIRouter(prefix="/messages", tags=["Messages"])
controller = Controller(router)


@controller.resource()
class MessageController:
    def __init__(
        self,
        database: AsyncIOMotorDatabase = Depends(get_db),
        nats: NatsConnection = Depends(get_nats),
    ):
        self.service = MessageService(database, nats)

    @controller.route.post("/", responses={201: {"description": "Message created"}})
    async def create_message(self, body: CreateMessageDto = Body(...)):
        """
        Create new message
        """
        return await self.service.create_message(body)

    @controller.route.get("/", responses={200: {"description": "List of messages"}})
    async def get_all_messages(self):
        """
        Get all messages
        """
        return await self.service.get_all_messages()
