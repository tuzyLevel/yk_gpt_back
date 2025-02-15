from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    id: str
    name: str
    email: str
    image: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class RequestPostCheckUser(BaseModel):
    email: str = Field(..., description="user_email")


class ResponsePostCheckUser(BaseModel):
    existed: bool = Field(..., description="ID info is existed?")
    data: Optional[UserSchema] = Field(None, description="사용자 정보")
