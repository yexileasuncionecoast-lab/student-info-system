"""Student service: CRUD operations backed by a JSON file."""
import json
import logging
import os
import tempfile
from pathlib import Path
from typing import List

from models.student import Student
from utils.exceptions import (
    DuplicateStudentError, StorageError, StudentNotFoundError, ValidationError,
)

logger = logging.getLogger("sis")


class StudentService:
    """Handles persistence and business rules for students."""

    def __init__(self, data_file: str):
        self.data_file = Path(data_file)
        self._students = {}  # student_id -> Student
        self._load()

    # ---------- persistence ----------
    def _load(self) -> None:
        """Read students from disk; start empty if the file doesn't exist."""
        if not self.data_file.exists():
            logger.info("Data file not found, starting empty: %s", self.data_file)
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
            for item in raw:
                s = Student.from_dict(item)
                self._students[s.student_id] = s
            logger.info("Loaded %d students", len(self._students))
        except (OSError, json.JSONDecodeError) as e:
            logger.error("Failed to read data file: %s", e)
            raise StorageError(f"Could not read data file: {e}")
        except ValidationError as e:
            logger.error("Corrupt record in data file: %s", e)
            raise StorageError(f"Data file contains an invalid record: {e}")

    def _save(self) -> None:
        """Write atomically so a crash can't leave a half-written file."""
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=self.data_file.parent, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in self._students.values()], f, indent=2)
            os.replace(tmp, self.data_file)
        except OSError as e:
            logger.error("Failed to save data: %s", e)
            raise StorageError(f"Could not save data: {e}")

    # ---------- CRUD ----------
    def add_student(self, student: Student) -> None:
        if student.student_id in self._students:
            raise DuplicateStudentError(f"Student ID '{student.student_id}' already exists.")
        self._students[student.student_id] = student
        self._save()
        logger.info("Added student %s", student.student_id)

    def get_student(self, student_id: str) -> Student:
        try:
            return self._students[student_id.strip()]
        except KeyError:
            raise StudentNotFoundError(f"No student with ID '{student_id}'.")

    def list_students(self) -> List[Student]:
        return sorted(self._students.values(), key=lambda s: s.student_id)

    def search_students(self, keyword: str) -> List[Student]:
        k = keyword.lower().strip()
        return [s for s in self.list_students()
                if k in s.name.lower() or k in s.course.lower()]

    def update_student(self, student_id: str, **changes) -> Student:
        """Update only the provided fields (name, age, course, email)."""
        current = self.get_student(student_id)
        data = current.to_dict()
        data.update({k: v for k, v in changes.items()
                     if k != "student_id" and v not in (None, "")})
        updated = Student.from_dict(data)  # re-validates
        self._students[current.student_id] = updated
        self._save()
        logger.info("Updated student %s", student_id)
        return updated

    def delete_student(self, student_id: str) -> None:
        student = self.get_student(student_id)
        del self._students[student.student_id]
        self._save()
        logger.info("Deleted student %s", student_id)
