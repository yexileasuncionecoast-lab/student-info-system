"""Command-line entry point for the Student Information System."""
import logging

from models.student import Student
from services.student_service import StudentService
from utils.config import load_config
from utils.exceptions import StudentError
from utils.logger import setup_logger

MENU = """
=== {title} ===
1. Add student
2. View all students
3. Search students
4. Update student
5. Delete student
0. Exit
"""


def add(service: StudentService) -> None:
    student = Student(
        student_id=input("Student ID: "),
        name=input("Name: "),
        age=input("Age: "),
        course=input("Course: "),
        email=input("Email: "),
    )
    service.add_student(student)
    print("Student added.")


def view_all(service: StudentService) -> None:
    students = service.list_students()
    if not students:
        print("No records found.")
    for s in students:
        print(s)


def search(service: StudentService) -> None:
    results = service.search_students(input("Search name or course: "))
    if not results:
        print("No matches.")
    for s in results:
        print(s)


def update(service: StudentService) -> None:
    sid = input("ID of student to update: ")
    print("Leave a field blank to keep its current value.")
    updated = service.update_student(
        sid,
        name=input("New name: "),
        age=input("New age: "),
        course=input("New course: "),
        email=input("New email: "),
    )
    print("Updated:", updated)


def delete(service: StudentService) -> None:
    sid = input("ID of student to delete: ")
    if input(f"Delete {sid}? (y/n): ").lower() == "y":
        service.delete_student(sid)
        print("Student deleted.")


ACTIONS = {"1": add, "2": view_all, "3": search, "4": update, "5": delete}


def main() -> None:
    config = load_config()
    logger = setup_logger(config["log_file"], config["log_level"])
    logger.info("Starting %s", config["app_name"])

    try:
        service = StudentService(config["data_file"])
    except StudentError as e:
        print(f"Startup error: {e}")
        return

    while True:
        print(MENU.format(title=config["app_name"]))
        choice = input("Choose an option: ").strip()
        if choice == "0":
            logger.info("Application closed")
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if not action:
            print("Invalid option.")
            continue
        try:
            action(service)
        except StudentError as e:  # expected, user-facing errors
            print(f"Error: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
        except Exception:  # unexpected: log full traceback
            logger.exception("Unexpected error")
            print("Something went wrong. See logs for details.")


if __name__ == "__main__":
    main()
