import aiosqlite

DB_PATH = "bots.db"


class BotDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS personalities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    creator_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS bot_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    personality_id INTEGER NOT NULL,
                    scenario TEXT,
                    initial_message TEXT,
                    FOREIGN KEY (personality_id) REFERENCES personalities (id)
                )
            ''')
            await db.commit()

    async def add_personality(self, creator_id: int, name: str, description: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO personalities (creator_id, name, description)
                    VALUES (?, ?, ?)
                ''', (creator_id, name, description))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def get_personalities(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT id, name, description
                FROM personalities
                WHERE creator_id = ?
            ''', (user_id,)) as cursor:
                return await cursor.fetchall()

    async def update_personality(self, personality_id: int, name: str, description: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    UPDATE personalities
                    SET name = ?, description = ?
                    WHERE id = ?
                ''', (name, description, personality_id))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def delete_personality(self, personality_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    DELETE FROM personalities
                    WHERE id = ?
                ''', (personality_id,))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def add_bot_info(self, personality_id: int, scenario: str, initial_message: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO bot_info (personality_id, scenario, initial_message)
                    VALUES (?, ?, ?)
                ''', (personality_id, scenario, initial_message))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def get_bot_info(self, personality_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT scenario, initial_message
                FROM bot_info
                WHERE personality_id = ?
            ''', (personality_id,)) as cursor:
                return await cursor.fetchone()

    async def update_bot_info(self, personality_id: int, scenario: str, initial_message: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    UPDATE bot_info
                    SET scenario = ?, initial_message = ?
                    WHERE personality_id = ?
                ''', (scenario, initial_message, personality_id))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def delete_bot_info(self, personality_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    DELETE FROM bot_info
                    WHERE personality_id = ?
                ''', (personality_id,))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()
