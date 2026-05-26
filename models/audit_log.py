from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC

from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False, index=True)
    student_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, default="SUCCESS")
    message = Column(String, nullable=True)
    timestamp = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True
    )