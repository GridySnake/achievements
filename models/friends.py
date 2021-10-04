import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class Friends:
    @staticmethod
    async def get_user_friends_suggestions(user_id: str, limit=20):
        conn = await asyncpg.connect(connection_url)
        users = await conn.fetch(f"""SELECT u.user_id, u.name, u.surname, img.href
                                     FROM users_information as u 
                                     LEFT JOIN images as img ON img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                     WHERE u.user_id not in (SELECT unnest(users_id) 
                                                       FROM friends 
                                                       WHERE user_id = {user_id})
                                     AND u.user_id <> {user_id}
                                     LIMIT {limit}
        """)
        return users

    @staticmethod
    async def get_user_friends_names(user_id: str, limit=20):
        conn = await asyncpg.connect(connection_url)
        users = await conn.fetch(f"""
                SELECT u.user_id, u.name, u.surname, a.href
                FROM users_information as u
                LEFT JOIN images as a
                    ON a.image_id = u.image_id[array_upper(u.image_id, 1)]
                WHERE u.user_id in (SELECT f.users_id[unnest(array_positions(f.status_id, 1))]
                                    FROM friends as f
                                    WHERE f.user_id = {user_id})
                LIMIT {limit}
            """)
        return users

    @staticmethod
    async def add_friend(user_active_id: str, user_passive_id: str):
        conn = await asyncpg.connect(connection_url)
        # тот кто кликает на добавить в друзья,
        # у него 0
        await conn.execute(f"""
            update friends
                set users_id = array_append(users_id, {user_passive_id}),
                    status_id = array_append(status_id, 0),
                    last_update = statement_timestamp()
            where user_id = {user_active_id}
        """)
        # тот у кого стоит заявка, у того 2
        await conn.execute(f"""
            update friends
                set users_id = array_append(users_id, {user_active_id}),
                    status_id = array_append(status_id, 2),
                    last_update = statement_timestamp()
            where user_id = {user_passive_id}
        """)

    @staticmethod
    async def friends_confirm(user_active_id: str,
                              user_passive_id: str,
                              confirm: bool):
        conn = await asyncpg.connect(connection_url)
        if confirm:
            print(confirm)
            await conn.execute(f"""
                update friends
                set status_id[array_position(users_id, {user_passive_id})] = 1
                where user_id = {user_active_id}
            """)
            result = await conn.execute(f"""
                update friends
                set status_id[array_position(users_id, {user_active_id})] = 1
                where user_id = {user_passive_id}
            """)
        else:
            result = await conn.execute(f"""
                update friends
                set status_id[array_position(users_id, {user_active_id})] = -1
                where user_id = {user_passive_id}
            """)
        return result

    @staticmethod
    async def block_friend(user_active_id: str,
                           user_passive_id: str):
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
            update friends
                set status_id[array_to_string(array_positions(status_id, 1), ',')::int] = -2
                --status_id[array_positions(status_id, 1)] = -2
            where user_id = {user_passive_id}
                and array_positions(status_id, 1) = array_positions(users_id, {user_active_id})
        """)
        await conn.execute(f"""
            update friends
                set status_id[array_to_string(array_positions(status_id, 1), ',')::int] = null,
                --status_id[array_positions(status_id, 1)] = null,
                    users_id[array_to_string(array_positions(users_id, {user_passive_id}), ',')::int] = null
                --users_id[array_positions(users_id, user_passive_id] = null
            where user_id = {user_active_id}
                and array_positions(status_id, 1) = array_positions(users_id, {user_passive_id})
        """)

    @staticmethod
    async def delete_friend(user_active_id: str,
                            user_passive_id: str):
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
                    update friends
                        set status_id[array_to_string(array_positions(status_id, 1), ',')::int] = 2
                        --status_id[array_positions(status_id, 1)] = 2
                    where user_id = {user_active_id}
                        and array_positions(status_id, 1) = array_positions(users_id, {user_passive_id})
                """)

        await conn.execute(f"""
            update friends
                set status_id[array_to_string(array_positions(status_id, 1), ',')::int] = -1
                --status_id[array_positions(status_id, 1)] = -1
            where user_id = {user_passive_id}
                and array_positions(status_id, 1) = array_positions(users_id, {user_active_id})
        """)

    @staticmethod
    async def get_subscribers(user_id: str):
        conn = await asyncpg.connect(connection_url)
        friends = await conn.fetch(f"""
                        select distinct(u.user_id), u.name, u.surname,
                        f.status_id[array_position(f.users_id, {user_id})] as status_id_passive,
                        img.href
                        from friends as f
                        inner join users_information as u on u.user_id = f.user_id
						left join images as img on img.image_id = u.image_id[array_upper(u.image_id, 1)]
                        where u.user_id in (
                                    select users_id[unnest(array_positions(f.status_id, 0))]
                                    FROM friends as f
                                    WHERE f.user_id = {user_id})
                        or
                        u.user_id in (
                                    select users_id[unnest(array_positions(f.status_id, 2))]
                                    FROM friends as f
                                    WHERE f.user_id = {user_id})
                        """)
        return friends
