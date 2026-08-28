"""
SQLite Local Persistence Manager for Hermes Studio
Database file path configurable via HERMES_DB_PATH.
Enforces WAL journal mode, Foreign Key constraints, and Subagent Audit Logging.
"""

import os
import sqlite3
import json
import uuid
from datetime import datetime

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "storage", "hermes_studio.db")
DB_PATH = os.getenv("HERMES_DB_PATH", r"D:\Hermes\HERMES-AHFMES-ECT\storage\hermes_studio.db")


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode and foreign key constraints
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        model TEXT NOT NULL,
        mode TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
    );
    """)

    # Subagent Audit Logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subagent_logs (
        id TEXT PRIMARY KEY,
        session_id TEXT,
        agent_name TEXT NOT NULL,
        action TEXT NOT NULL,
        evidence TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def create_session(title="New Conversation", model="hermes-v0.2", mode="architect"):
    conn = get_db()
    session_id = str(uuid.uuid4())
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (id, title, model, mode) VALUES (?, ?, ?, ?)",
        (session_id, title, model, mode)
    )
    conn.commit()
    conn.close()
    return {"id": session_id, "title": title, "model": model, "mode": mode}


def list_sessions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions ORDER BY updated_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_messages(session_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE session_id = ? ORDER BY created_at ASC", (session_id,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def add_message(session_id, role, content, metadata=None):
    conn = get_db()
    cursor = conn.cursor()
    msg_id = str(uuid.uuid4())
    meta_json = json.dumps(metadata) if metadata else None
    cursor.execute(
        "INSERT INTO messages (id, session_id, role, content, metadata) VALUES (?, ?, ?, ?, ?)",
        (msg_id, session_id, role, content, meta_json)
    )
    cursor.execute("UPDATE sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()
    return {"id": msg_id, "session_id": session_id, "role": role, "content": content}


def log_subagent_execution(session_id, agent_name, action, evidence):
    """Persists subagent audit execution log into subagent_logs table."""
    conn = get_db()
    cursor = conn.cursor()
    log_id = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO subagent_logs (id, session_id, agent_name, action, evidence) VALUES (?, ?, ?, ?, ?)",
        (log_id, session_id, agent_name, action, evidence)
    )
    conn.commit()
    conn.close()


def delete_session(session_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()


# Initialize database schema on load
init_db()
