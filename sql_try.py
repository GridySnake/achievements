import asyncpg
from asyncpgsa import pg
from config.common import BaseConfig
async def a():
    await pg.init(
        host=BaseConfig.host,
        port=BaseConfig.port,
        database=BaseConfig.database_name,
        user=BaseConfig.user,
        password=BaseConfig.password
    )
    user = await dict(pg.fetchrow(f"""
            SELECT * 
            FROM users
            WHERE email = 'kunilov-aleksandr2011@yandex.ru'
            """))
    print(user)
if __name__ == 'main':
    a()