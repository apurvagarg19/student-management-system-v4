from database import Base, engine
from models import student, subject, student_marks

Base.metadata.create_all(bind=engine)

print("✅ Database and tables created!")