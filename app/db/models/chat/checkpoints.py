from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from ...database import Base


class Checkpoints(Base):
    __tablename__ = "chat_checkpoints"
    session_id = Column(String, primary_key=True)
    state = Column(JSONB, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<Checkpoint(session_id={self.session_id}, timestamp={self.timestamp})>"
