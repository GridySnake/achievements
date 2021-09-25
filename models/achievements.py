import asyncpgsa
from config.common import BaseConfig
import asyncpg
database = asyncpgsa.create_pool(
        host=BaseConfig.host,
        port=BaseConfig.port,
        database=BaseConfig.database_name,
        user=BaseConfig.user,
        password=BaseConfig.password
    )


class Achievements:
    @staticmethod
    async def get_user_achievements(user_id: str):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        achievements = await conn.fetch(f"""
        SELECT name, description
        FROM achievements
        WHERE {user_id} = ANY(user_id)
        """)
        return achievements

    @staticmethod
    async def create_new_achievement(user_id: str, name: str, description: str):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        id = await conn.fetchrow(f"""
                SELECT MAX(achievement_id)
                FROM achievements
                """)
        id = int(dict(id)['max']) + 1
        if name and description:
            await conn.execute(f"""
                insert INTO achievements (achievement_id, user_id, name, description, creator_id) values(
                {id}, ARRAY[]::integer[], '{name}', '{description}', {user_id})
                """)
