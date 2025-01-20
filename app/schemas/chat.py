from pydantic import BaseModel, Field


class ChatLine(BaseModel):
    key: str = Field(..., description="chat key")
    chat_id: str | None = Field(None, description="chat_id")
    writer: str = Field(..., description="sender")
    message: str = Field(..., description="message from sender")
