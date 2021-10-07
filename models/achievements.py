import asyncpg
from config.common import BaseConfig

connection_url = BaseConfig.database_url


class Achievements:
    @staticmethod
    async def get_created_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
        select name, description
        from achievements
        where user_id = {user_id}
        """)
        return achievements

    @staticmethod
    async def get_suggestion_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
            select a.user_id, a.name as title, a.description, a.created_date, a.new, u.name, u.surname
            from achievements as a
            inner join users_information as u on u.user_id = a.user_id
            where a.user_id <> {user_id}
            """)
        return achievements

    @staticmethod
    async def create_new_achievement(user_id: str, name: str, description: str):
        conn = await asyncpg.connect(connection_url)
        id = await conn.fetch(f"""
                select max(achievement_id)
                from achievements
                """)
        id = dict(id[0])['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        if name and description:
            await conn.execute(f"""
                insert into achievements (achievement_id, user_id, name, description, created_date, new) values(
                {id}, {user_id}, '{name}', '{description}', statement_timestamp(), true)
                """)
