from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileRequest(Base):
    __tablename__ = "file_requests"

    id = Column(String, primary_key=True, index=True)
    user_hash = Column(String)
    user_name = Column(String)
    file = Column(String)
    deny_reason = Column(String)
    request_body = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    state = Column(String, default="pending")
