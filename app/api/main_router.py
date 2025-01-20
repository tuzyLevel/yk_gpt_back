from fastapi import APIRouter
from .chat.router import chat_router
from .user.router import user_router

main_router = APIRouter()


main_router.include_router(
    chat_router,
    prefix="/chat",
)

main_router.include_router(
    user_router,
    prefix="/user",
)
