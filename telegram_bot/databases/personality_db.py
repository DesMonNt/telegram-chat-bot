import aiosqlite

DB_PATH = "personalities.db"


class PersonalityDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS personalities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    UNIQUE(user_id, name)
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER PRIMARY KEY,
                    active_personality TEXT
                )
            ''')
            await db.commit()

    async def add_personality(self, user_id: int, name: str, description: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO personalities (user_id, name, description)
                    VALUES (?, ?, ?)
                ''', (user_id, name, description))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def get_personalities(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT name, description FROM personalities WHERE user_id = ?', (user_id,)) as cursor:
                return await cursor.fetchall()

    async def update_personality(self, user_id: int, name: str, new_description: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    UPDATE personalities
                    SET description = ?
                    WHERE user_id = ? AND name = ?
                ''', (new_description, user_id, name))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def delete_personality(self, user_id: int, name: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    DELETE FROM personalities
                    WHERE user_id = ? AND name = ?
                ''', (user_id, name))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def set_active_personality(self, user_id: int, name: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO user_settings (user_id, active_personality)
                    VALUES (?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET active_personality = ?
                ''', (user_id, name, name))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def get_active_personality(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT active_personality FROM user_settings WHERE user_id = ?', (user_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else None
