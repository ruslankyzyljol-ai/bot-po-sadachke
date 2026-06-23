"""
database.py
Колдонуучулардын маалыматын сактоо үчүн жөнөкөй SQLite база.
"""
import aiosqlite
from datetime import datetime


class Database:
    def __init__(self, path: str):
        self.path = path
        self._conn: aiosqlite.Connection | None = None

    async def init(self):
        self._conn = await aiosqlite.connect(self.path)
        await self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                full_name   TEXT,
                language    TEXT DEFAULT NULL,
                joined_at   TEXT
            )
            """
        )
        await self._conn.commit()

    async def add_user_if_not_exists(self, user_id: int, username: str, full_name: str):
        cur = await self._conn.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        if row is None:
            await self._conn.execute(
                "INSERT INTO users (user_id, username, full_name, joined_at) VALUES (?, ?, ?, ?)",
                (user_id, username, full_name, datetime.utcnow().isoformat()),
            )
            await self._conn.commit()
            return True  # жаңы колдонуучу
        return False

    async def set_language(self, user_id: int, language: str):
        await self._conn.execute(
            "UPDATE users SET language = ? WHERE user_id = ?", (language, user_id)
        )
        await self._conn.commit()

    async def get_language(self, user_id: int) -> str | None:
        cur = await self._conn.execute(
            "SELECT language FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cur.fetchone()
        if row is None:
            return None
        return row[0]

    async def get_all_user_ids(self) -> list[int]:
        cur = await self._conn.execute("SELECT user_id FROM users")
        rows = await cur.fetchall()
        return [r[0] for r in rows]

    async def count_users(self) -> int:
        cur = await self._conn.execute("SELECT COUNT(*) FROM users")
        row = await cur.fetchone()
        return row[0] if row else 0

    async def close(self):
        if self._conn:
            await self._conn.close()
