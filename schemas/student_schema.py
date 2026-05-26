from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Dict, Optional, List, Any


# ---------------- BASE SCHEMA ----------------

class BaseMarksSchema(BaseModel):
    marks: Dict[str, float] = Field(
        ...,
        description="Dictionary of subject and marks",
        json_schema_extra={"example": {"math": 85, "science": 90}}
    )

    @field_validator("marks")
    def validate_marks(cls, marks):
        if not marks:
            raise ValueError("Marks cannot be empty")

        for subject, mark in marks.items():
            if not subject.strip():
                raise ValueError("Subject name cannot be empty")

            if not (0 <= mark <= 100):
                raise ValueError(f"{subject} must be between 0 and 100")

        return marks


# ---------------- REQUEST SCHEMAS ----------------

class StudentCreateSchema(BaseMarksSchema):
    student_id: str = Field(..., min_length=1,max_length=20, json_schema_extra={"example": "S101"})
    name: str = Field(..., min_length=2, max_length=50, json_schema_extra={"example": "Apurva"})


class UpdateMarksSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    marks: Optional[Dict[str, float]] = None
    
    #concurrency control field
    version: Optional[int] = Field(
        None,
        ge=1
    )

    @field_validator("marks")
    def validate_marks(cls, marks):
        if marks is None:
            return marks

        if not marks:
            raise ValueError("Marks cannot be empty")

        for subject, mark in marks.items():
            if not subject.strip():
                raise ValueError("Subject name cannot be empty")

            if not (0 <= mark <= 100):
                raise ValueError(f"{subject} must be between 0 and 100")

        return marks


# ---------------- RESPONSE SCHEMA ----------------

class SubjectMarks(BaseModel):
    subject: str
    marks: float


class StudentResponseSchema(BaseModel):
    student_id: str
    name: str
    total_marks: float
    percentage: float
    grade: str
    
    version: int
    
    marks: List[SubjectMarks]

    model_config = ConfigDict(
        from_attributes=True
    )
    
#------------------------STANDARD API RESPONSE------------------------

class APIResponse(BaseModel):
    success: bool = True
    message: str = "Operation successful"
    data: Optional[Any] = None


# ---------------- ERROR RESPONSE ----------------

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    data: Optional[Any] = None