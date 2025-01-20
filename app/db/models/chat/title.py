from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ...database import Base


class Title(Base):
    __tablename__ = "title"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(50), index=True)
    email = Column(String(255), nullable=False)
    title = Column(String(100), default="New Chat")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
