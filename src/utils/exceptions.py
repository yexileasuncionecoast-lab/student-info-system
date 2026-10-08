"""Custom exceptions used across the application."""


class StudentError(Exception):
    """Base class for all application errors."""


class ValidationError(StudentError):
    """Raised when student data is invalid."""


class StudentNotFoundError(StudentError):
    """Raised when a student ID does not exist."""


class DuplicateStudentError(StudentError):
    """Raised when adding a student whose ID already exists."""


class StorageError(StudentError):
    """Raised when reading or writing the data file fails."""
