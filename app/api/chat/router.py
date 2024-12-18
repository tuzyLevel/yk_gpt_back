from fastapi import APIRouter
from app.services.chat.base import chat
from .schema import RequestChat, ResponseChat

chat_router = APIRouter(
    tags=["chat"],
)


@chat_router.post("")
async def request_chat(req: RequestChat) -> ResponseChat:
    return await chat(question=req.question)
