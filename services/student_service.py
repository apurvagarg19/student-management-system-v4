import logging

from typing import Dict, Optional

from sqlalchemy.orm import Session, joinedload

from schemas.student_schema import UpdateMarksSchema

from models.student import Student
from models.subject import Subject
from models.student_marks import StudentMarks
from models.audit_log import AuditLog

from utils.cache import cache


logger = logging.getLogger(__name__)


class StudentService:

    def __init__(self, db: Session):
        self.db = db

    # ---------------- CACHE ----------------

    def invalidate_cache(self):

        cache.invalidate("topper")
        cache.invalidate("rank_list")

    # ---------------- CALCULATION ----------------

    def calculate(self, marks: Dict[str, float]):

        total = float(sum(marks.values()))

        percentage = total / len(marks)

        if percentage >= 90:
            grade = "A"

        elif percentage >= 75:
            grade = "B"

        elif percentage >= 60:
            grade = "C"

        elif percentage >= 40:
            grade = "D"

        else:
            grade = "F"

        return total, percentage, grade

    # ---------------- COMMON FILTER ----------------

    def apply_filters(
        self,
        query,
        name,
        grade,
        min_percentage,
        max_percentage,
        failed
    ):

        if name:
            query = query.filter(
                Student.name.ilike(f"%{name}%")
            )

        if grade:
            query = query.filter(
                Student.grade == grade
            )

        if min_percentage is not None:
            query = query.filter(
                Student.percentage >= min_percentage
            )

        if max_percentage is not None:
            query = query.filter(
                Student.percentage <= max_percentage
            )

        if failed is True:
            query = query.filter(
                Student.grade == "F"
            )

        elif failed is False:
            query = query.filter(
                Student.grade != "F"
            )

        return query

    # ---------------- CREATE ----------------

    def add_student(
        self,
        student_id: str,
        name: str,
        marks: Dict[str, float]
    ):

        existing_student = (
            self.db.query(Student)
            .filter_by(student_id=student_id)
            .first()
        )

        if existing_student:
            raise ValueError("Student already exists")

        total, percentage, grade = self.calculate(marks)

        try:

            with self.db.begin_nested():

                student = Student(
                    student_id=student_id,
                    name=name,
                    total_marks=total,
                    percentage=percentage,
                    grade=grade,
                    version=1
                )
                

                self.db.add(student)

                existing_subjects = {
                    s.name: s
                    for s in self.db.query(Subject)
                    .filter(
                        Subject.name.in_(marks.keys())
                    )
                    .all()
                }

                for subject_name, mark in marks.items():

                    subject = existing_subjects.get(
                        subject_name
                    )

                    if not subject:

                        subject = Subject(
                            name=subject_name
                        )

                        self.db.add(subject)

                        self.db.flush()

                    self.db.add(
                        StudentMarks(
                            student_id=student_id,
                            subject_id=subject.id,
                            marks=mark
                        )
                    )

                audit = AuditLog(
                    action="CREATE",
                    student_id=student_id,
                    status="SUCCESS",
                    message="Student created successfully"
                )

                self.db.add(audit)
                
            self.db.commit()

            self.invalidate_cache()

            logger.info(
                f"Student added: {student_id}"
            )

        except Exception:
            
            self.db.rollback()

            logger.exception(
                f"Failed to add student: {student_id}"
            )

            raise

    # ---------------- READ ----------------

    def get_student(self, student_id: str):

        student = (
            self.db.query(Student)
            .options(
                joinedload(Student.marks)
                .joinedload(StudentMarks.subject)
            )
            .filter_by(student_id=student_id)
            .first()
        )

        if not student:
            raise ValueError("Student not found")

        return student

    def get_all_students(self):

        return (
            self.db.query(Student)
            .all()
        )

    def get_students(
        self,
        page: int,
        limit: int,
        name: Optional[str] = None,
        grade: Optional[str] = None,
        min_percentage: Optional[float] = None,
        max_percentage: Optional[float] = None,
        failed: Optional[bool] = None
    ):

        query = (
            self.db.query(Student)
            .options(
                joinedload(Student.marks)
                .joinedload(StudentMarks.subject)
            )
        )

        query = self.apply_filters(
            query,
            name,
            grade,
            min_percentage,
            max_percentage,
            failed
        )

        return (
            query.offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    def get_total_students_count(
        self,
        name: Optional[str] = None,
        grade: Optional[str] = None,
        min_percentage: Optional[float] = None,
        max_percentage: Optional[float] = None,
        failed: Optional[bool] = None
    ) -> int:

        query = self.db.query(Student)

        query = self.apply_filters(
            query,
            name,
            grade,
            min_percentage,
            max_percentage,
            failed
        )

        return query.count()

    # ---------------- UPDATE ----------------

    def update_student(
        self,
        student_id: str,
        data: UpdateMarksSchema
    ):

        student = self.get_student(student_id)

        try:

            with self.db.begin_nested():

                # Optimistic locking
                if (
                    data.version is not None
                    and student.version != data.version
                ):
                    raise ValueError(
                        "Student was modified by another request"
                    )

                if data.name:
                    student.name = data.name

                if data.marks:

                    self.db.query(StudentMarks).filter_by(
                        student_id=student_id
                    ).delete()

                    existing_subjects = {
                        s.name: s
                        for s in self.db.query(Subject)
                        .filter(
                            Subject.name.in_(
                                data.marks.keys()
                            )
                        )
                        .all()
                    }

                    for subject_name, mark in data.marks.items():

                        subject = existing_subjects.get(
                            subject_name
                        )

                        if not subject:

                            subject = Subject(
                                name=subject_name
                            )

                            self.db.add(subject)

                            self.db.flush()

                        self.db.add(
                            StudentMarks(
                                student_id=student_id,
                                subject_id=subject.id,
                                marks=mark
                            )
                        )

                    total, percentage, grade = (
                        self.calculate(data.marks)
                    )

                    student.total_marks = total
                    student.percentage = percentage
                    student.grade = grade

                # Increment version
                student.version += 1

                audit = AuditLog(
                    action="UPDATE",
                    student_id=student_id,
                    status="SUCCESS",
                    message="Student updated successfully"
                )

                self.db.add(audit)

            self.db.commit()
            self.invalidate_cache()

            logger.info(
                f"Student updated: {student_id}"
            )

        except Exception:
            self.db.rollback()

            logger.exception(
                f"Failed to update student: {student_id}"
            )

            raise

    # ---------------- DELETE ----------------

    def delete_student(self, student_id: str):

        student = self.get_student(student_id)

        try:

            with self.db.begin_nested():

                self.db.delete(student)

                audit = AuditLog(
                    action="DELETE",
                    student_id=student_id,
                    status="SUCCESS",
                    message="Student deleted successfully"
                )

                self.db.add(audit)

            self.db.commit()
            self.invalidate_cache()

            logger.info(
                f"Student deleted: {student_id}"
            )

        except Exception:

            self.db.rollback()

            logger.exception(
                f"Failed to delete student: {student_id}"
            )

            raise

    # ---------------- ANALYTICS ----------------

    def get_topper(self):

        cached = cache.get("topper")

        if cached:
            return cached

        student = (
            self.db.query(Student)
            .order_by(Student.percentage.desc())
            .first()
        )

        if not student:
            raise ValueError(
                "No students available"
            )

        cache.set("topper", student, ttl=60)

        return student

    def get_average_percentage(self):

        students = (
            self.db.query(Student)
            .all()
        )

        if not students:
            return 0.0

        return (
            sum(s.percentage for s in students)
            / len(students)
        )

    def get_ranked_list(self):

        cached = cache.get("rank_list")

        if cached:
            return cached

        students = (
            self.db.query(Student)
            .order_by(
                Student.percentage.desc(),
                Student.name.asc()
            )
            .all()
        )

        cache.set("rank_list", students, ttl=60)

        return students

    # ---------------- SUBJECT ANALYSIS ----------------

    def get_subject_analysis(self):

        results = (
            self.db.query(
                Subject.name,
                StudentMarks.marks
            )
            .join(
                StudentMarks,
                Subject.id == StudentMarks.subject_id
            )
            .all()
        )

        if not results:
            return {}

        data = {}

        for subject, mark in results:
            data.setdefault(subject, []).append(mark)

        return {
            subject: {
                "highest": max(marks),
                "average": (
                    sum(marks) / len(marks)
                )
            }
            for subject, marks in data.items()
        }

    # ---------------- DASHBOARD ----------------

    def dashboard(self):

        students = (
            self.db.query(Student)
            .all()
        )

        if not students:

            return {
                "total_students": 0,
                "pass_percentage": 0,
                "grades": {
                    "A": 0,
                    "B": 0,
                    "C": 0,
                    "D": 0,
                    "F": 0
                },
                "average_percentage": 0,
                "topper": None
            }

        grades = {
            g: 0
            for g in ["A", "B", "C", "D", "F"]
        }

        for student in students:
            grades[student.grade] += 1

        passed = sum(
            1
            for s in students
            if s.grade != "F"
        )

        topper = max(
            students,
            key=lambda s: s.percentage
        )

        return {
            "total_students": len(students),
            "pass_percentage": (
                passed / len(students)
            ) * 100,
            "grades": grades,
            "average_percentage": (
                self.get_average_percentage()
            ),
            "topper": topper.name
        }

    # ---------------- RESPONSE FORMAT ----------------

    def format_student(self, student):

        return {
            "student_id": student.student_id,
            "name": student.name,
            "total_marks": student.total_marks,
            "percentage": student.percentage,
            "grade": student.grade,
            "version": student.version,
            "marks": [
                {
                    "subject": m.subject.name,
                    "marks": m.marks
                }
                for m in student.marks
            ]
        }