from app.database import Base, engine
from models import student, subject, student_marks, audit_log


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Database and tables created!")