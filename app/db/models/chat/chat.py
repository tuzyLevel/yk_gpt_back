from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ...database import Base


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(50), index=True)
    user_id = Column(String(100))
    message = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
