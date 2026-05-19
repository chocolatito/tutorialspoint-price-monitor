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
SCRIPT_T1 = """CREATE TABLE IF NOT EXISTS monitor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id TEXT,
    href TEXT,
    title TEXT,
    data_title TEXT,
    price REAL,
    old_price REAL,
    profile TEXT,
    profile_url TEXT,
    available INTEGER
);"""
SCRIPT_T2 = """CREATE TABLE IF NOT EXISTS historical (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price REAL NOT NULL,
    date DATETIME NOT NULL,
    monitor_id INTEGER NOT NULL,

    FOREIGN KEY (monitor_id)
        REFERENCES monitor(id)
        ON DELETE CASCADE
);"""
SCRIPT_LIST = [
    "PRAGMA foreign_keys = ON;",
    SCRIPT_T1,
    SCRIPT_T2,
]
