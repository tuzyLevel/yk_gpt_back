from sqlalchemy.orm import Session
from app.db.models.user import User


def get_user_by_id(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()
