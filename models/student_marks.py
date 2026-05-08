from sqlalchemy import Column, Integer, Float, ForeignKey,String, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class StudentMarks(Base):
    __tablename__ = "student_marks"
    
    __table_args__ = (
        UniqueConstraint("student_id", "subject_id", name="unique_student_subject"),
    )
    id = Column(Integer, primary_key=True)

    student_id = Column(String, ForeignKey("students.student_id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)

    marks = Column(Float, index=True)

    student = relationship("Student", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")