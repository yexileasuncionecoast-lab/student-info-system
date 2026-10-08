import pytest

from models.student import Student
from services.student_service import StudentService
from utils.exceptions import (
    DuplicateStudentError, StudentNotFoundError, ValidationError,
)


@pytest.fixture
def service(tmp_path):
    return StudentService(str(tmp_path / "students.json"))


def make(sid="S1", name="Ana Cruz"):
    return Student(sid, name, 20, "BSIT", "ana@example.com")


def test_add_and_get(service):
    service.add_student(make())
    assert service.get_student("S1").name == "Ana Cruz"


def test_persistence(tmp_path):
    path = str(tmp_path / "s.json")
    StudentService(path).add_student(make())
    assert len(StudentService(path).list_students()) == 1


def test_duplicate_rejected(service):
    service.add_student(make())
    with pytest.raises(DuplicateStudentError):
        service.add_student(make())


def test_update(service):
    service.add_student(make())
    assert service.update_student("S1", course="BSCS").course == "BSCS"


def test_delete(service):
    service.add_student(make())
    service.delete_student("S1")
    with pytest.raises(StudentNotFoundError):
        service.get_student("S1")


def test_validation():
    with pytest.raises(ValidationError):
        Student("S2", "Bob", 20, "BSIT", "not-an-email")
    with pytest.raises(ValidationError):
        Student("S2", "Bob", "abc", "BSIT", "b@x.com")
