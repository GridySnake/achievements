import asyncpg
import datetime
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class Goals:
    @staticmethod
    async def get_goals(user_id: str = None,
                        community_id: str = None):
        if user_id is not None:
            table = 'users_information'
            ident = int(user_id)
            column_name = 'user_id'
        if community_id is not None:
            table = 'communities'
            ident = int(community_id)
            column_name = 'community_id'
        conn = await asyncpg.connect(connection_url)
        goals = await conn.fetch(f"""
            select a.name, a.achievement_id
            from achievements a 
            right join (
                select unnest(achievements_desired_id) as desired_id 
                from {table} 
                where {column_name}={ident}
                ) as u 
                on u.desired_id = a.achievement_id
                """)
        return goals

    # @staticmethod
    # async def get_goals_for_community(user_id: str, community_id: str):
    #     user_id = int(user_id)
    #     community_id = int(community_id)


