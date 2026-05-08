import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from services.student_service import StudentService


# ---------------- TEST DB SETUP ----------------

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def service(db):
    return StudentService(db)


@pytest.fixture
def sample_students(service):
    service.add_student("1", "Alice", {"math": 50})
    service.add_student("2", "Bob", {"math": 90})
    return service


# ---------------- HELPER ----------------

class DummyUpdate:
    def __init__(self, name=None, marks=None):
        self.name = name
        self.marks = marks


# ---------------- CREATE ----------------

def test_add_student(service):
    service.add_student("1", "A", {"math": 90})

    students = service.get_students(1, 100)
    assert len(students) == 1
    assert students[0].student_id == "1"


def test_duplicate_student(service):
    service.add_student("1", "A", {"math": 90})

    with pytest.raises(ValueError):
        service.add_student("1", "A", {"math": 90})


# ---------------- READ ----------------

def test_get_student(service):
    service.add_student("1", "A", {"math": 90})

    student = service.get_student("1")

    assert student.name == "A"


def test_get_student_not_found(service):
    with pytest.raises(ValueError):
        service.get_student("999")


def test_get_all_students(sample_students):
    students = sample_students.get_all_students()
    assert len(students) == 2


# ---------------- UPDATE ----------------

def test_update_marks(service):
    service.add_student("1", "A", {"math": 50})

    service.update_student("1", DummyUpdate(marks={"math": 100}))

    student = service.get_student("1")
    assert student.percentage == 100


def test_update_name_only(service):
    service.add_student("1", "OldName", {"math": 80})

    service.update_student("1", DummyUpdate(name="NewName"))

    student = service.get_student("1")
    assert student.name == "NewName"


def test_update_non_existing(service):
    with pytest.raises(ValueError):
        service.update_student("999", DummyUpdate(marks={"math": 80}))


# ---------------- DELETE ----------------

def test_delete_student(service):
    service.add_student("1", "A", {"math": 90})

    service.delete_student("1")

    assert service.get_all_students() == []


def test_delete_non_existing(service):
    with pytest.raises(ValueError):
        service.delete_student("999")


# ---------------- FILTERING ----------------

def test_filter_by_grade(sample_students):
    result = sample_students.get_students(1, 10, grade="A")

    assert len(result) == 1
    assert result[0].grade == "A"


def test_filter_by_min_percentage(sample_students):
    result = sample_students.get_students(1, 10, min_percentage=60)

    assert len(result) == 1
    assert result[0].student_id == "2"


def test_filter_by_max_percentage(sample_students):
    result = sample_students.get_students(1, 10, max_percentage=80)

    assert len(result) == 1
    assert result[0].student_id == "1"


def test_filter_failed(service):
    service.add_student("1", "A", {"math": 30})
    service.add_student("2", "B", {"math": 80})

    result = service.get_students(1, 10, failed=True)

    assert len(result) == 1
    assert result[0].grade == "F"


def test_filter_passed(service):
    service.add_student("1", "A", {"math": 30})
    service.add_student("2", "B", {"math": 80})

    result = service.get_students(1, 10, failed=False)

    assert len(result) == 1
    assert result[0].grade != "F"


def test_search_by_name(service):
    service.add_student("1", "Alice", {"math": 90})

    result = service.get_students(1, 10, name="alice")

    assert len(result) == 1
    assert result[0].name == "Alice"


def test_pagination(sample_students):
    result = sample_students.get_students(page=1, limit=1)

    assert len(result) == 1


# ---------------- ANALYTICS ----------------

def test_topper(sample_students):
    topper = sample_students.get_topper()
    assert topper.student_id == "2"


def test_topper_empty(service):
    with pytest.raises(ValueError):
        service.get_topper()


def test_average(sample_students):
    avg = sample_students.get_average_percentage()
    assert avg == 70.0


def test_ranked_list(sample_students):
    ranks = sample_students.get_ranked_list()

    assert ranks[0].student_id == "2"
    assert ranks[1].student_id == "1"


# ---------------- SUBJECT ANALYSIS ----------------

def test_subject_analysis(service):
    service.add_student("1", "A", {"math": 90, "science": 80})
    service.add_student("2", "B", {"math": 70, "science": 60})

    result = service.get_subject_analysis()

    assert result["math"]["highest"] == 90
    assert result["science"]["highest"] == 80
    assert "average" in result["math"]


def test_subject_analysis_empty(service):
    assert service.get_subject_analysis() == {}


# ---------------- DASHBOARD ----------------

def test_dashboard(sample_students):
    result = sample_students.dashboard()

    assert result["total_students"] == 2
    assert result["topper"] == "Bob"
    assert result["grades"]["A"] == 1


def test_dashboard_empty(service):
    result = service.dashboard()

    assert result["total_students"] == 0
    assert result["topper"] is None