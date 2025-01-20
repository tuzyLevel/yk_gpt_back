from app.db.models.chat.title import Title
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import desc


async def get_titles_by_email(email: str, db: Session) -> List[Title]:
    return (
        db.query(Title)
        .filter(Title.email == email)
        .order_by(desc(Title.created_at))
        .all()
    )
