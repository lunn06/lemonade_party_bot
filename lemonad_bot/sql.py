import sqlite3
import aiosqlite
from config import DB_NAME

class DB:

    def __init__(self, db_name):
        self.db_name = db_name

        with sqlite3.connect(self.db_name) as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS user (
                    uid TEXT UNIQUE,
                    lottery INTEGER UNIQUE,
                    points INTEGER,
                    star BOOLEAN,
                    super_star BOOLEAN
                )"""
            )

            cur.execute("""CREATE TABLE IF NOT EXISTS user_code (
                    uid TEXT,
                    code TEXT UNIQUE,
                    station TEXT
                )"""
            )

            cur.commit()

    @classmethod
    async def create(cls, db_name):
        self = DB()
        self.db_name = db_name
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS user (
                    uid TEXT UNIQUE,
                    lottery INTEGER UNIQUE,
                    points INTEGER,
                    star BOOLEAN,
                    super_star BOOLEAN
                )"""
            )

            await db.execute("""CREATE TABLE IF NOT EXISTS user_code (
                    uid TEXT,
                    code TEXT UNIQUE,
                    station TEXT
                )"""
            )

            await db.commit()
        return self

    async def insert_user(self, uid, lottery, points, star, super_star):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                    "INSERT INTO user VALUES (?, ?, ?, ?, ?)",
                    (uid, lottery, points, star, super_star)
                )

            await db.commit()

    async def insert_data(self, uid, code, station):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                    "INSERT INTO user_code VALUES (?, ?, ?)",
                    (uid, code, station)
                )

            await db.commit()


    async def get_user(self, uid):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM user WHERE (user.uid = ?)", (uid,)) as cur:
                async for row in cur:
                    row_user = list(row)
        
        return {
            'uid': row_user[0],
            'lottery': row_user[1],
            'points': row_user[2],
            'star': row_user[3],
            'super_star': row_user[4],
        }

    async def get_data(self, uid): 
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM user_code WHERE (user_code.uid = ?)", (uid,)) as cur:
                row_user_data = list(await cur.fetchall())

        response = []
        for (uid, code, station) in row_user_data:
            response.append({
                'uid': uid,
                'code': code,
                'station': station,
            })

        return response
    
    async def change_points(self, uid, new_points):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                    "UPDATE user SET points = ? WHERE uid = ?",
                    (new_points, uid)
                )

            await db.commit()

    async def change_star(self, uid, new_star):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                    "UPDATE user SET star = ? WHERE uid = ?",
                    (new_star, uid)
                )

            await db.commit()

    async def change_super_star(self, uid, new_super_star):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                    "UPDATE user SET super_star = ? WHERE uid = ?",
                    (new_super_star, uid)
                )

            await db.commit()


if __name__ == "__main__":
    import asyncio

    async def main():
        db = DB('test.db')
        await db.insert_user('123', 123, 0, False, False)
        await db.insert_data('123', '123', 'gift')
        await db.insert_data('123', '133', 'gift')
        print(await db.get_user('123'))
        for k in await db.get_data('123'):
            print(k)

    asyncio.run(main())

