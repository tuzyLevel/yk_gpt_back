from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class RequestChat(BaseModel):
    question: str = Field(..., description="user question")


class ResponseChat(BaseModel):
    answer: str = Field(..., description="AI answer")


class TitleSchema(BaseModel):
    email: str
    chat_id: str
    title: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class ResponseGetTitles(BaseModel):
    titles: List[dict]
