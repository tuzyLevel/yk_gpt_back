from ..ai.chains.chain import chain
from sqlalchemy.orm import Session
from app.db.models.chat.chat import Chat
from typing import TypedDict, List


async def chat(question: str):
    return chain.invoke({"message": question})


async def get_chat_by_id(chat_id: str, db: Session):
    db_chat = (
        db.query(Chat).filter(Chat.chat_id == chat_id).order_by(Chat.created_at).all()
    )
    return db_chat


async def insert_chat(chat_id: str, writer: str, message: str, db: Session):
    new_chat = Chat(chat_id=chat_id, message=message, user_id=writer)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat
