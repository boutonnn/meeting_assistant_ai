from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class MeetingInformation(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, index=True)
    content = Column(Text)
    summary = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
