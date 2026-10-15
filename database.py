import os
import sqlite3
from contextlib import contextmanager

DATABASE_PATH = os.getenv("DATABASE_PATH", "orchestrator.db")

@contextmanager
def connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with connection() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            repository_url TEXT NOT NULL,
            jira_project_key TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")

def list_projects():
    with connection() as db:
        rows = db.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]

def create_project(name, repository_url, jira_project_key=""):
    name = (name or "").strip()
    repository_url = (repository_url or "").strip()
    jira_project_key = (jira_project_key or "").strip()
    if not name or not repository_url:
        raise ValueError("Project name and repository URL are required.")
    if not repository_url.startswith("https://"):
        raise ValueError("Repository URL must be an HTTPS URL.")
    with connection() as db:
        cursor = db.execute("INSERT INTO projects (name, repository_url, jira_project_key) VALUES (?, ?, ?)", (name, repository_url, jira_project_key))
        row = db.execute("SELECT * FROM projects WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return dict(row)

def delete_project(project_id):
    with connection() as db:
        cursor = db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        return cursor.rowcount > 0
