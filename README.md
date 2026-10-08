# Student Information System

A cloud-ready, command-line Student Information System written in Python.
Student records are stored in JSON and managed through a simple CRUD menu.

## Features
- Add, view, search, update and delete students
- JSON data storage with atomic writes (no half-written files)
- Input validation (age range, email format, required fields)
- Configuration via `config/config.json` with environment-variable overrides
- File + console logging and custom exception handling
- Unit tests with pytest

## Project Structure
```
student-info-system/
├── src/
│   ├── models/student.py            # Student dataclass + validation
│   ├── services/student_service.py  # CRUD + JSON persistence
│   ├── utils/                       # config, logger, exceptions
│   └── main.py                      # CLI entry point
├── data/students.json               # data store
├── config/config.json               # settings
├── logs/                            # runtime logs (git-ignored)
├── tests/                           # pytest tests
├── requirements.txt
└── README.md
```

## Getting Started
```bash
git clone https://github.com/<your-username>/student-info-system.git
cd student-info-system
pip install -r requirements.txt
python src/main.py
```

## Configuration
Edit `config/config.json`, or override with environment variables:

| Variable | Purpose | Default |
|---|---|---|
| `SIS_DATA_FILE` | Path to JSON data file | `data/students.json` |
| `SIS_LOG_FILE` | Path to log file | `logs/app.log` |
| `SIS_LOG_LEVEL` | DEBUG / INFO / WARNING / ERROR | `INFO` |

## Running Tests
```bash
pytest
```

## Sample Record
```json
{ "student_id": "2024-001", "name": "Ana Cruz", "age": 20,
  "course": "BSIT", "email": "ana@example.com" }
```

## Cloud Readiness
Configuration is externalised, logging is centralised, storage is isolated in
one service class (easy to swap for S3/DynamoDB/a database), and errors are
handled without crashing the app.

## Author
<Your Name>
