from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
