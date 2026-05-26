from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    CheckConstraint,
    Index
)

from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):

    __tablename__ = "students"

    __table_args__ = (

        CheckConstraint(
            "percentage >= 0 AND percentage <= 100",
            name="check_percentage_range"
        ),

        Index(
            "idx_grade_percentage",
            "grade",
            "percentage"
        ),
    )

    student_id = Column(
        String,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    total_marks = Column(
        Float,
        nullable=False,
        default=0,
        index=True
    )

    percentage = Column(
        Float,
        nullable=False,
        default=0,
        index=True
    )

    grade = Column(
        String,
        nullable=False,
        index=True
    )
    version = Column(
        Integer,
        nullable=False,
        default=1
    )

    # Relationships
    marks = relationship(
        "StudentMarks",
        back_populates="student",
        cascade="all, delete-orphan"
    )