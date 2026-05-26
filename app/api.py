import logging

from typing import Dict, Any

from fastapi import (
    FastAPI,
    Depends,
    Query
)

from fastapi.responses import JSONResponse

from fastapi.exceptions import (
    RequestValidationError
)

from sqlalchemy.orm import Session

from app.database import SessionLocal

from schemas.student_schema import (
    StudentCreateSchema,
    UpdateMarksSchema,
    APIResponse
)

from services.student_service import StudentService

from middleware.logging_middleware import (
    LoggingMiddleware
)

from middleware.rate_limit import (
    RateLimitMiddleware
)

from utils.response import (
    success_response,
    error_response
)

from services.ai_service import AIService
from utils.cache import cache



# ---------------- LOGGING ----------------

logging.basicConfig(
    filename="student_management.log",
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)

logger = logging.getLogger(__name__)


# ---------------- APP INIT ----------------

app = FastAPI(
    title="Student Management API",
    description=(
        "API for managing "
        "students and marks"
    ),
    version="5.0.0"
)


# ---------------- MIDDLEWARE ----------------

app.add_middleware(
    LoggingMiddleware
)

app.add_middleware(
    RateLimitMiddleware
)


# ---------------- GLOBAL EXCEPTION HANDLERS ----------------

@app.exception_handler(Exception)
async def global_exception_handler(
    request,
    exc
):
    import traceback

    logger.exception(str(exc))
    
    print("\n=====BACKEND ERROR=====")
    traceback.print_exc()
    print("=======================\n")

    return JSONResponse(
        status_code=500,
        content=error_response(
            message=str(exc)
        )
    )


@app.exception_handler(
    RequestValidationError
)
async def validation_exception_handler(
    request,
    exc
):

    return JSONResponse(
        status_code=422,
        content=error_response(
            message="Validation failed",
            data=exc.errors()
        )
    )


# ---------------- DATABASE DEPENDENCY ----------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_service(
    db: Session = Depends(get_db)
):

    return StudentService(db)


# ---------------- HEALTH CHECK ----------------

@app.get(
    "/",
    tags=["Health"],
    response_model=APIResponse
)
def home():

    return success_response(
        message="Student Management API is running"
    )


# ---------------- CREATE ----------------

@app.post(
    "/students",
    tags=["Students"],
    response_model=APIResponse,
    status_code=201
)
def add_student(
    data: StudentCreateSchema,
    service: StudentService = Depends(get_service)
):

    service.add_student(
        data.student_id,
        data.name,
        data.marks
    )

    return success_response(
        message="Student added successfully"
    )


# ---------------- READ ----------------

@app.get(
    "/students",
    tags=["Students"],
    response_model=Dict[str, Any]
)
def get_students(

    page: int = Query(1, ge=1),

    limit: int = Query(
        10,
        ge=1,
        le=100
    ),

    name: str = Query(None),

    grade: str = Query(None),

    min_percentage: float = Query(
        None,
        ge=0,
        le=100
    ),

    max_percentage: float = Query(
        None,
        ge=0,
        le=100
    ),

    failed: bool = Query(None),

    service: StudentService = Depends(get_service)
):

    if (
        min_percentage is not None
        and max_percentage is not None
        and min_percentage > max_percentage
    ):
        return JSONResponse(
            status_code=400,
            content=error_response(
                "min_percentage cannot be greater than max_percentage"
            )
        )

    students = service.get_students(
        page,
        limit,
        name,
        grade,
        min_percentage,
        max_percentage,
        failed
    )

    total = service.get_total_students_count(
        name,
        grade,
        min_percentage,
        max_percentage,
        failed
    )

    return success_response(
        data={
            "page": page,
            "limit": limit,
            "total": total,
            "students": [
                service.format_student(s)
                for s in students
            ]
        },
        message="Students fetched successfully"
    )





# ---------------- UPDATE ----------------

@app.put(
    "/students/{student_id}",
    tags=["Students"],
    response_model=APIResponse
)
def update_student(
    student_id: str,
    data: UpdateMarksSchema,
    service: StudentService = Depends(get_service)
):

    service.update_student(
        student_id,
        data
    )

    return success_response(
        message="Student updated successfully"
    )


# ---------------- DELETE ----------------

@app.delete(
    "/students/{student_id}",
    tags=["Students"],
    response_model=APIResponse
)
def delete_student(
    student_id: str,
    service: StudentService = Depends(get_service)
):

    service.delete_student(student_id)

    return success_response(
        message="Student deleted successfully"
    )


# ---------------- ANALYTICS ----------------

@app.get(
    "/students/topper",
    tags=["Analytics"],
    response_model=APIResponse
)
def get_topper(
    service: StudentService = Depends(get_service)
):

    student = service.get_topper()

    return success_response(
        data=service.format_student(student),
        message="Topper fetched successfully"
    )


@app.get(
    "/students/average",
    tags=["Analytics"],
    response_model=APIResponse
)
def get_average(
    service: StudentService = Depends(get_service)
):

    return success_response(
        data={
            "average_percentage":
            service.get_average_percentage()
        },
        message="Average percentage fetched successfully"
    )


@app.get(
    "/students/rank-list",
    tags=["Analytics"],
    response_model=APIResponse
)
def get_rank_list(
    service: StudentService = Depends(get_service)
):

    return success_response(
        data=[
            service.format_student(s)
            for s in service.get_ranked_list()
        ],
        message="Rank list fetched successfully"
    )


@app.get(
    "/students/dashboard",
    tags=["Analytics"],
    response_model=APIResponse
)
def get_dashboard(
    service: StudentService = Depends(get_service)
):

    return success_response(
        data=service.dashboard(),
        message="Dashboard fetched successfully"
    )


@app.get(
    "/students/subject-analysis",
    tags=["Analytics"],
    response_model=APIResponse
)
def subject_analysis(
    service: StudentService = Depends(get_service)
):

    return success_response(
        data=service.get_subject_analysis(),
        message="Subject analysis fetched successfully"
    )
    
@app.get(
    "/students/{student_id}",
    tags=["Students"],
    response_model=APIResponse
)
def get_student(
    student_id: str,
    service: StudentService = Depends(get_service)
):

    student = service.get_student(student_id)

    return success_response(
        data=service.format_student(student),
        message="Student fetched successfully"
    )
    
@app.get(
    "/students/{student_id}/insights",
    tags=["AI"],
    response_model=APIResponse
)
def get_student_insights(
    student_id: str,
    service: StudentService = Depends(get_service)
):

    cache_key = f"insights_{student_id}"

    cached = cache.get(cache_key)

    if cached:

        return success_response(
            data=cached,
            message="Insights fetched from cache"
        )

    student = service.get_student(student_id)

    try:
        insights = AIService.generate_student_insights(
            student
        )

    except Exception as e:
        return error_response(
            message=f"AI insight generation failed: {str(e)}"
        )

    cache.set(
        cache_key,
        insights,
        ttl=300
    )

    return success_response(
        data=insights,
        message="Student insights generated"
    )
    
@app.post(
    "/ai/query",
    tags=["AI"],
    response_model=APIResponse
)
def ai_query(
    payload: dict,
    service: StudentService = Depends(get_service)
):

    query = payload.get("query")

    if not query:

        return error_response(
            message="Query is required"
        )

    allowed_keywords = [
        "student",
        "marks",
        "grade",
        "percentage",
        "top",
        "failed",
        "average"
    ]

    if not any(
        word in query.lower()
        for word in allowed_keywords
    ):

        return error_response(
            message=(
                "Only academic queries "
                "are allowed"
            )
        )

    students = service.get_all_students()

    student_context = "\n".join([

        f"""
        Name: {s.name}
        Percentage: {s.percentage}
        Grade: {s.grade}
        """

        for s in students
    ])

    prompt = f"""
    You are NovaMind AI.

    Use ONLY the provided student data.

    Student Data:
    {student_context}

    User Query:
    {query}
    """

    try:
        reply = AIService.ask_ai(prompt)

    except Exception as e:
        return error_response(
            message=f"AI service failed: {str(e)}"
        )

    return success_response(
        data={
            "reply": reply
        },
        message="AI query processed"
    )
    
@app.get(
    "/ai/report",
    tags=["AI"],
    response_model=APIResponse
)
def generate_ai_report(
    service: StudentService = Depends(get_service)
):

    cache_key = "ai_class_report"

    cached = cache.get(cache_key)

    if cached:

        return success_response(
            data=cached,
            message="Report fetched from cache"
        )

    students = service.get_all_students()

    try:
        report = AIService.generate_class_report(
            students
        )

    except Exception as e:
        return error_response(
            message=f"AI report generation failed: {str(e)}"
        )

    cache.set(
        cache_key,
        report,
        ttl=300
    )

    return success_response(
        data=report,
        message="AI report generated"
    )


@app.post(
    "/ai/chat",
    tags=["AI"],
    response_model=APIResponse
)
def chat_with_ai(
    payload: dict,
    service: StudentService = Depends(get_service)
):

    user_message = payload.get("message")

    if not user_message:

        return error_response(
            message="Message is required"
        )
        
    allowed_keywords = [
        "student",
        "marks",
        "grade",
        "percentage",
        "topper",
        "performance",
        "subject",
        "average",
        "failed"
    ]

    if not any(
        word in user_message.lower()
        for word in allowed_keywords
   ):

        return error_response(
            message=(
                "Only student management "
                "queries are allowed"
            )
        )

    # Fetch all students from database
    students = service.get_all_students()

    # Build student context
    student_context = "\n".join([

        f"""
        Student ID: {s.student_id}
        Name: {s.name}
        Percentage: {s.percentage}
        Grade: {s.grade}
        Total Marks: {s.total_marks}
        """

        for s in students
    ])


    prompt = f"""
    You are NovaMind AI for Student Management.

    Use ONLY the provided student data.

    Do NOT invent information.

    Reject unrelated questions politely.

    STUDENT DATABASE:
    {student_context}

    USER QUESTION:
    {user_message}
    """

    try:
        reply = AIService.ask_ai(prompt)

    except Exception as e:
        return error_response(
            message=f"AI service failed: {str(e)}"
        )

    return success_response(
        data={
            "reply": reply
        },
        message="AI response generated"
    )