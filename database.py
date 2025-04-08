import sqlite3
from datetime import datetime

class ThreatDatabase:
    def __init__(self, db_name="threat_data.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                response TEXT,
                created_at TEXT
            )''')

    def save_threat(self, query, response):
        with self.conn:
            self.conn.execute(
                "INSERT INTO threats (query, response, created_at) VALUES (?, ?, ?)",
                (query, response, datetime.utcnow().isoformat())
            )

    def get_all_threats(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM threats ORDER BY created_at DESC")
            return cursor.fetchall()
