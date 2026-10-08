"""Student data model with validation."""
import re
from dataclasses import dataclass, asdict

from utils.exceptions import ValidationError

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class Student:
    """Represents a single student record."""
    student_id: str
    name: str
    age: int
    course: str
    email: str

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        """Raise ValidationError if any field is invalid."""
        self.student_id = str(self.student_id).strip()
        self.name = str(self.name).strip()
        self.course = str(self.course).strip()
        self.email = str(self.email).strip()

        if not self.student_id:
            raise ValidationError("Student ID is required.")
        if not self.name:
            raise ValidationError("Name is required.")
        try:
            self.age = int(self.age)
        except (TypeError, ValueError):
            raise ValidationError("Age must be a whole number.")
        if not 5 <= self.age <= 120:
            raise ValidationError("Age must be between 5 and 120.")
        if not self.course:
            raise ValidationError("Course is required.")
        if not EMAIL_RE.match(self.email):
            raise ValidationError("Email address is not valid.")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        try:
            return cls(
                student_id=data["student_id"],
                name=data["name"],
                age=data["age"],
                course=data["course"],
                email=data["email"],
            )
        except KeyError as e:
            raise ValidationError(f"Missing field in record: {e}")

    def __str__(self) -> str:
        return (f"[{self.student_id}] {self.name}, {self.age} yrs | "
                f"{self.course} | {self.email}")
