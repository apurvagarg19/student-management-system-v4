import logging
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from database import SessionLocal
from schemas.student_schema import (
    StudentCreateSchema,
    StudentResponseSchema,
    UpdateMarksSchema,
    MessageResponse
)
from services.student_service import StudentService

# ---------------- LOGGING ----------------

logging.basicConfig(
    filename="student_management.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------- APP INIT ----------------

app = FastAPI(
    title="Student Management API",
    description="API for managing students and their marks",
    version="1.0.0"
)

# ---------------- DEPENDENCIES ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db: Session = Depends(get_db)):
    return StudentService(db)


# ---------------- HEALTH CHECK ----------------

@app.get("/", tags=["Health"], summary="Health check")
def home():
    return {
        "status": "success",
        "message": "Student Management API is running"
    }


# ---------------- CREATE ----------------

@app.post(
    "/students",
    tags=["Students"],
    response_model=MessageResponse,
    status_code=201,
    summary="Create a new student",
    description="Add a new student with subject-wise marks"
)
def add_student(
    data: StudentCreateSchema,
    service: StudentService = Depends(get_service)
):
    try:
        service.add_student(data.student_id, data.name, data.marks)
        logger.info(f"Student added: {data.student_id}")
        return MessageResponse(message="Student added successfully")

    except ValueError as e:
        logger.exception("Add student failed")
        raise HTTPException(status_code=400, detail=str(e))


# ---------------- READ ----------------

@app.get(
    "/students",
    tags=["Students"],
    response_model=Dict[str, Any],
    summary="Get students",
    description="""
Retrieve students with:
- Pagination (page, limit)
- Search by name
- Filter by grade
- Filter by percentage range
- Filter failed/passed students
""",
    response_description="Paginated list of students"
)
def get_students(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Records per page"),
    name: str = Query(None, description="search by name"),
    grade: str = Query(None, description="filter by grade"),
    min_percentage: float = Query(None, ge=0, le=100, description="minimum percentage"),
    max_percentage: float = Query(None, ge=0, le=100, description="maximum percentage"),
    failed: bool = Query(None, description="True = failed, False = passed"),
    service: StudentService = Depends(get_service)
):
    
    if min_percentage is not None and max_percentage is not None:
        if min_percentage > max_percentage:
            raise HTTPException(
                status_code=400,
                detail="min_percentage cannot be greater than max_percentage"
            )

    try:
        students = service.get_students(
            page, limit, name, grade, min_percentage, max_percentage, failed
        )

        total = service.get_total_students_count(
            name, grade, min_percentage, max_percentage, failed
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": [service.format_student(s) for s in students]
        }

    except Exception as e:
        logger.exception("Failed to fetch students")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get(
    "/students/{student_id}",
    tags=["Students"],
    response_model=StudentResponseSchema,
    summary="Get student by ID"
)
def get_student(
    student_id: str,
    service: StudentService = Depends(get_service),
):
    try:
        student = service.get_student(student_id)
        return service.format_student(student)

    except ValueError as e:
        logger.exception("Get student failed")
        raise HTTPException(status_code=404, detail=str(e))


# ---------------- UPDATE ----------------

@app.put(
    "/students/{student_id}",
    tags=["Students"],
    response_model=MessageResponse,
    summary="Update student"
)
def update_student(
    student_id: str,
    data: UpdateMarksSchema,
    service: StudentService = Depends(get_service)
):
    try:
        service.update_student(student_id, data)
        logger.info(f"Student updated: {student_id}")
        return MessageResponse(message="Student updated successfully")

    except ValueError as e:
        logger.exception("Update failed")
        raise HTTPException(status_code=404, detail=str(e))


# ---------------- DELETE ----------------

@app.delete(
    "/students/{student_id}",
    tags=["Students"],
    status_code=204,
    summary="Delete a student"
)
def delete_student(
    student_id: str,
    service: StudentService = Depends(get_service)
):
    try:
        service.delete_student(student_id)
        logger.info(f"Student deleted: {student_id}")
        return

    except ValueError as e:
        logger.exception("Delete failed")
        raise HTTPException(status_code=404, detail=str(e))


# ---------------- ANALYTICS ----------------

@app.get(
    "/students/topper",
    tags=["Analytics"],
    response_model=StudentResponseSchema,
    summary="Get top-performing student"
)
def get_topper(service: StudentService = Depends(get_service)):
    student = service.get_topper()
    return service.format_student(student)


@app.get(
    "/students/average",
    tags=["Analytics"],
    summary="Get average percentage"
)
def get_average(service: StudentService = Depends(get_service)):
    return {"average_percentage": service.get_average_percentage()}


@app.get(
    "/students/rank-list",
    tags=["Analytics"],
    response_model=List[StudentResponseSchema],
    summary="Get ranked students"
)
def get_rank_list(service: StudentService = Depends(get_service)):
    return [service.format_student(s) for s in service.get_ranked_list()]


@app.get(
    "/students/dashboard",
    tags=["Analytics"],
    summary="Get dashboard statistics"
)
def get_dashboard(service: StudentService = Depends(get_service)):
    return service.dashboard()


@app.get(
    "/students/subject-analysis",
    tags=["Analytics"],
    summary="Get subject-wise analysis"
)
def subject_analysis(service: StudentService = Depends(get_service)):
    return service.get_subject_analysis()