from pydantic import BaseModel
from typing import Any

class CreateMessageDto(BaseModel):
    source: str
    content: dict[str, Any]
