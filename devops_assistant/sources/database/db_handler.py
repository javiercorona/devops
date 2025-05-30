import sqlite3
from typing import Optional

class DBHandler:
    def __init__(self, db_path: str = "artifacts.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._ensure_table()

    def _ensure_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS artifacts (
                    key TEXT PRIMARY KEY,
                    code TEXT NOT NULL
                )
            """)

    def save_artifact(self, key: str, code: str):
        with self.conn:
            self.conn.execute(
                "REPLACE INTO artifacts (key, code) VALUES (?, ?)",
                (key, code)
            )

    def get_artifact(self, key: str) -> Optional[str]:
        cur = self.conn.cursor()
        cur.execute("SELECT code FROM artifacts WHERE key = ?", (key,))
        row = cur.fetchone()
        return row[0] if row else ""

    @property
    def store(self):
        # For listing keys
        cur = self.conn.cursor()
        cur.execute("SELECT key FROM artifacts")
        return [r[0] for r in cur.fetchall()]
