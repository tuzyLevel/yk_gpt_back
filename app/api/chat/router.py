from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.chat.base import chat, get_chat_by_id
from app.services.title import get_titles_by_email
from app.core.swagger_auth import get_current_username
from app.db.database import get_db


from .schema import RequestChat, ResponseChat, ResponseGetTitles, TitleSchema


chat_router = APIRouter(
    tags=["chat"],
)


@chat_router.post("", dependencies=[Depends(get_current_username)])
async def request_chat(req: RequestChat) -> ResponseChat:
    return await chat(question=req.question)


@chat_router.get("/{chat_id}", dependencies=[Depends(get_current_username)])
async def request_get_chat_by_id(chat_id: str, db: Session = Depends(get_db)):
    chat = await get_chat_by_id(chat_id, db=db)
    return chat


@chat_router.get("/titles/{email}", dependencies=[Depends(get_current_username)])
async def request_get_titles(email: str, db: Session = Depends(get_db)):
    titles = await get_titles_by_email(email, db=db)
    return ResponseGetTitles(
        titles=[TitleSchema.model_validate(title).model_dump() for title in titles]
    )
