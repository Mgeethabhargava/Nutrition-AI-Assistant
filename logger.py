# logger.py

import sqlite3
from datetime import datetime
from typing import Optional

DB_NAME = "logs.db"
DB_PATH = "chat_logs.db"

def init_log_db():
    """Initialize the logging database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Function to log prompt/response
def log_prompt_response(username: str, user_input: str, agent_response: str):
    timestamp = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, username, prompt, response)
        VALUES (?, ?, ?, ?)
    """, (timestamp, username, user_input, agent_response))
    conn.commit()
    conn.close()

def log_interaction(username: str, prompt: str, response: str):
    """Insert a new prompt/response pair."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (username, prompt, response, timestamp) VALUES (?, ?, ?, ?)",
        (username, prompt, response, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def fetch_user_logs(username: str):
    """Fetch previous logs of a user."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT prompt, response, timestamp FROM logs WHERE username = ? ORDER BY timestamp DESC", (username,))
    results = c.fetchall()
    conn.close()
    return results

def clear_logs(username: Optional[str] = None):
    """Clear logs for a user or all."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if username:
        c.execute("DELETE FROM logs WHERE username = ?", (username,))
    else:
        c.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
