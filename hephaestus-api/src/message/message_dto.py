from pydantic import BaseModel


class RatifyMessageDto(BaseModel):
    messageId: str
