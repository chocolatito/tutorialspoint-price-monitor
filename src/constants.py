from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(".env")
BASE_DIR = str(Path(__file__).parents[1])
LOG_NAME = f"{Path(__file__).parents[1].parts[-1]}.log"
FILE_DIR = "FILES"
HEADERS = {'accept-language': 'en;q=0.9'}
PROXY = os.getenv("PROXY", None)
DB_NAME = "MONITOR.db"
SCRIPT_T1 = """CREATE TABLE IF NOT EXISTS course (
    course_id TEXT PRIMARY KEY,
    href TEXT,
    title TEXT,
    data_title TEXT,
    sale_price REAL,
    list_price REAL,
    profile TEXT,
    profile_url TEXT,
    available INTEGER,
    hexdigest TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);"""
SCRIPT_T1_1 = """CREATE TRIGGER IF NOT EXISTS update_course_timestamp
    AFTER UPDATE ON course
    BEGIN
        UPDATE course SET updated_at = CURRENT_TIMESTAMP WHERE course_id = OLD.course_id;
    END;"""
SCRIPT_T2 = """CREATE TABLE IF NOT EXISTS historical (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_price REAL NOT NULL,
    list_price REAL NOT NULL,
    course_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id)
        REFERENCES course(course_id)
        ON DELETE CASCADE
);"""

SCRIPT_LIST = [
    "PRAGMA foreign_keys = ON;",
    SCRIPT_T1,
    SCRIPT_T1_1,
    SCRIPT_T2,
]
