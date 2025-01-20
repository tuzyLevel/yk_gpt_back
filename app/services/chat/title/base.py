from sqlalchemy.orm import Session
from app.db.models.chat.title import Title
from typing import TypedDict, List
from ...ai.title.chain import chain


async def get_title(chat_id: str, db=Session) -> Title | None:
    title: Title = db.query(Title).filter(Title.chat_id == chat_id).first()
    if title:
        return title
    else:
        return None


async def get_titles_by_id(email: str, db=Session) -> List[Title]:
    title_list: List[Title] = db.query(Title).filter(Title.email == email).all()
    return title_list


async def insert_title(chat_id: str, title: str, email: str, db=Session):
    new_title = Title(chat_id=chat_id, title=title, email=email)
    db.add(new_title)
    db.commit()
    db.refresh(new_title)
    return new_title


async def make_new_title(first_user_question: str, first_ai_answer: str):
    return chain.invoke(
        {"user_question": first_user_question, "ai_answer": first_ai_answer}
    )
