from pydantic import BaseModel
from typing import Any

class CreateMessageDto(BaseModel):
    source: str
    txt: str
    ratified: bool = False
    content: dict[str, Any]


class RatifyMessageDto(BaseModel):
    message_id: str
    merchant_id: str
