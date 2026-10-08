"""Configuration management: loads settings from config/config.json.

Environment variables (SIS_DATA_FILE, SIS_LOG_FILE, SIS_LOG_LEVEL) override
the file values, which makes the app easy to run in containers / cloud hosts.
"""
import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT_DIR / "config" / "config.json"

DEFAULTS = {
    "app_name": "Student Information System",
    "data_file": "data/students.json",
    "log_file": "logs/app.log",
    "log_level": "INFO",
}


def load_config(path: Path = CONFIG_PATH) -> dict:
    """Load config from JSON, falling back to defaults on any problem."""
    config = dict(DEFAULTS)
    try:
        with open(path, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    except (OSError, json.JSONDecodeError):
        pass  # use defaults; logger is not configured yet

    # Environment overrides
    config["data_file"] = os.getenv("SIS_DATA_FILE", config["data_file"])
    config["log_file"] = os.getenv("SIS_LOG_FILE", config["log_file"])
    config["log_level"] = os.getenv("SIS_LOG_LEVEL", config["log_level"])

    # Resolve relative paths against the project root
    for key in ("data_file", "log_file"):
        p = Path(config[key])
        config[key] = str(p if p.is_absolute() else ROOT_DIR / p)
    return config
