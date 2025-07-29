# diary_db.py

import sqlite3
from datetime import datetime

DB_NAME = "diary.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Chat logs table
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            query TEXT,
            response TEXT,
            timestamp TEXT
        )
    """)

    # Meal logs table
    c.execute("""
        CREATE TABLE IF NOT EXISTS meal_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            meal TEXT,
            nutrients TEXT,
            timestamp TEXT
        )
    """)

    # Meal diary table
    c.execute("""
        CREATE TABLE IF NOT EXISTS meal_diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            meal TEXT,
            calories TEXT,
            notes TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

def log_chat(username, query, response):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO chat_logs (username, query, response, timestamp)
        VALUES (?, ?, ?, ?)
    """, (username, query, response, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def log_meal(username, meal, nutrients):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO meal_logs (username, meal, nutrients, timestamp)
        VALUES (?, ?, ?, ?)
    """, (username, meal, nutrients, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def log_meal_diary(user: str, meal: str, calories: str, notes: str = ""):
    """Logs meal data into meal_diary table."""
    timestamp = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO meal_diary (user, meal, calories, notes, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user, meal, calories, notes, timestamp))
    conn.commit()
    conn.close()

def insert_entry(user: str, meal: str, calories: str, notes: str = ""):
    """Alias for log_meal_diary for compatibility."""
    log_meal_diary(user, meal, calories, notes)

def get_chat_history(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT query, response, timestamp
        FROM chat_logs
        WHERE username=?
        ORDER BY id DESC
    """, (username,))
    results = c.fetchall()
    conn.close()
    return results

def fetch_meal_diary(user: str):
    """Returns meal diary logs for a user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT meal, calories, notes, timestamp
        FROM meal_diary
        WHERE user=?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def clear_meal_diary(user: str = None):
    """Deletes meal diary logs. If user is provided, deletes only their logs."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if user:
        cursor.execute("DELETE FROM meal_diary WHERE user=?", (user,))
    else:
        cursor.execute("DELETE FROM meal_diary")
    conn.commit()
    conn.close()