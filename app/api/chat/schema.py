from pydantic import BaseModel, Field


class RequestChat(BaseModel):
    question: str = Field(..., description="user question")


class ResponseChat(BaseModel):
    answer: str = Field(..., description="AI answer")
