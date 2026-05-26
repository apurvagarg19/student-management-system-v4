from app.database import Base, engine

from models import (
    student,
    subject,
    student_marks,
    audit_log
)

Base.metadata.create_all(bind=engine)

print("Database and tables created!")