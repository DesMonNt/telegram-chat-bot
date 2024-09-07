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
                    scenario TEXT,
                    initial_message TEXT,
                    FOREIGN KEY (id) REFERENCES personalities (id)
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

    async def add_bot_info(self, bot_id: int, scenario: str, initial_message: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO bot_info (id, scenario, initial_message)
                    VALUES (?, ?, ?)
                ''', (bot_id, scenario, initial_message))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def get_bot_info(self, bot_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT scenario, initial_message
                FROM bot_info
                WHERE id = ?
            ''', (bot_id,)) as cursor:
                return await cursor.fetchone()

    async def update_bot_scenario(self, bot_id: int, scenario: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    UPDATE bot_info
                    SET scenario = ?
                    WHERE id = ?
                ''', (scenario, bot_id))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def update_bot_initial_message(self, bot_id: int, initial_message: str):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    UPDATE bot_info
                    SET initial_message = ?
                    WHERE id = ?
                ''', (initial_message, bot_id))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def delete_bot_info(self, bot_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    DELETE FROM bot_info
                    WHERE id = ?
                ''', (bot_id,))
                await db.commit()
            except aiosqlite.Error:
                await db.rollback()

    async def get_description(self, user_id: int, name: str):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT description
                FROM personalities
                WHERE creator_id = ? AND name = ?
            ''', (user_id, name)) as cursor:
                result = await cursor.fetchone()
                return result[0]

    async def get_bot_scenario(self, bot_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT scenario
                FROM bot_info
                WHERE id = ?
            ''', (bot_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0]

    async def get_bot_initial_message(self, bot_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT initial_message
                FROM bot_info
                WHERE id = ?
            ''', (bot_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0]
