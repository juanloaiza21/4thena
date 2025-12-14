from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi_router_controller import Controller

from src.deps import get_db, get_nats
from src.message.message_service import MessageService
from src.message.message_dto import RatifyMessageDto
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

    @controller.route.post("/ratify", responses={201: {"description": "Message ratified"}})
    async def ratify_message(self, body: RatifyMessageDto = Body(...)):
        """
        Ratify a message
        """
        return await self.service.ratify_message(body.message_id)

    @controller.route.get("/list", responses={200: {"description": "List of messages"}})
    async def list_messages(self):
        """
        List all unratified messages
        """
        return await self.service.get_unratified_messages()
