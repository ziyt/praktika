
import sqlite3

from .paths import DB_PATH

def _unicode_lower(s):
    return s.lower() if isinstance(s, str) else s

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.create_function("LOWER", 1, _unicode_lower)
    return conn
