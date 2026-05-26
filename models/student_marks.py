from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    String,
    UniqueConstraint,
    CheckConstraint,
    Index
)

from sqlalchemy.orm import relationship

from app.database import Base


class StudentMarks(Base):

    __tablename__ = "student_marks"

    __table_args__ = (

        UniqueConstraint(
            "student_id",
            "subject_id",
            name="unique_student_subject"
        ),

        CheckConstraint(
            "marks >= 0 AND marks <= 100",
            name="check_valid_marks"
        ),

        Index(
            "idx_student_subject",
            "student_id",
            "subject_id"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        String,
        ForeignKey("students.student_id"),
        nullable=False,
        index=True
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False,
        index=True
    )

    marks = Column(
        Float,
        nullable=False,
        index=True
    )

    student = relationship(
        "Student",
        back_populates="marks"
    )

    subject = relationship(
        "Subject",
        back_populates="marks"
    )