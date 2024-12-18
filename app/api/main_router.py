from fastapi import APIRouter
from .chat.router import chat_router

main_router = APIRouter()


main_router.include_router(
    chat_router,
    prefix="/chat",
)
