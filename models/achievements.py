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
    async def get_reached_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
            select a.name, a.description
            from (select user_id, unnest(achievements_id) as achievements_id from users_information) as u
            inner join achievements as a on u.achievements_id = a.achievement_id
            where u.user_id = {user_id}
            """)
        return achievements

    @staticmethod
    async def update_user_info_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        data = await conn.fetch(f"""
                                select a.achievement_id, c.parameter, c.value
                                from (select achievement_id, unnest(conditions) as conditions from achievements) as a
                                inner join achi_conditions as c on text(c.condition_id) = a.conditions
                                where achi_condition_group_id = 0  and a.achievement_id not in (select unnest(achievements_id) as achievements_id from users_information where user_id = {user_id})
        """)
        for i in data:
            if i['value'].isdigit():
                await conn.execute(f"""
                                    update users_information
                                    set achievements_id = array_append(achievements_id, {i['achievement_id']})
                                    where user_id = {user_id} and {i['parameter']} = {i['value']} and {i['achievement_id']} not in (
                                        select unnest(achievements_id) from users_information where user_id = {user_id})
                                    """)
            else:
                await conn.execute(f"""
                                    update users_information
                                    set achievements_id = array_append(achievements_id, {i['achievement_id']})
                                    where user_id = {user_id} and {i['parameter']} = '{i['value']}' and {i['achievement_id']} not in (
                                        select unnest(achievements_id) from users_information where user_id = {user_id})
                                   """)

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
    async def create_new_achievement(user_id: str, data):
        if data['value'] != '' and data['name'] != '' and data['description'] != '':
            conn = await asyncpg.connect(connection_url)
            id_achi = await conn.fetch(f"""
                    select max(achievement_id)
                    from achievements
                    """)
            id_achi = dict(id_achi[0])['max']
            if id_achi is not None:
                id_achi = int(id_achi) + 1
            else:
                id_achi = 0
            id_condi = await conn.fetch(f"""
                                select max(condition_id)
                                from achi_conditions
                                """)
            id_condi = dict(id_condi[0])['max']
            if id_condi is not None:
                id_condi = int(id_condi) + 1
            else:
                id_condi = 0
            await conn.execute(f"""
                            insert into achi_conditions (condition_id, parameter, value, achi_condition_group_id) values(
                            {id_condi}, '{data['select_parameter']}', '{data['value']}', {data['select_group']})
                            """)
            await conn.execute(f"""
                insert into achievements (achievement_id, user_id, name, description, conditions, created_date, new) values(
                {id_achi}, {user_id}, '{data['name']}', '{data['description']}', ARRAY['{id_condi}'], statement_timestamp(), true)
                """)
            if data['value'].isdigit():
                await conn.execute(f"""
                                   update users_information
                                   set achievements_id = array_append(achievements_id, {id_achi})
                                   where user_id in (
                                   select user_id
                                   from users_information
                                   where {data['select_parameter']} = {data['value']})
                                   """)
            else:
                await conn.execute(f"""
                                update users_information
                                set achievements_id = array_append(achievements_id, {id_achi})
                                where user_id in (
                                select user_id
                                from users_information
                                where {data['select_parameter']} = '{data['value']}')
                                """)
