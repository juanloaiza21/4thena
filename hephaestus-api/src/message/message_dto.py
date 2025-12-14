from pydantic import BaseModel


class RatifyMessageDto(BaseModel):
    message_id: str
