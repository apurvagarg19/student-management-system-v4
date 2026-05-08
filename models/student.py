from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    total_marks = Column(Float, index=True)
    percentage = Column(Float, index=True)
    grade = Column(String, index=True)

    marks = relationship("StudentMarks", back_populates="student", cascade="all, delete")