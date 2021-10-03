import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class Friends:
    @staticmethod
    async def get_user_friends_suggestions(user_id: str, limit=20):
        conn = await asyncpg.connect(connection_url)
        users = await conn.fetch(f"""SELECT u.user_id, u.name, u.surname, img.href
                                     FROM users_information as u 
                                     LEFT JOIN images as img ON img.image_id = ANY(u.image_id)
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
                WHERE u.user_id in (SELECT unnest(f.users_id)
                                    FROM friends as f
                                    WHERE 1 = any(f.status_id)
                                        and f.user_id = {user_id})
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
        user_active_id = int(user_active_id)
        user_passive_id = int(user_passive_id)
        conn = await asyncpg.connect(connection_url)
        if confirm:
            await conn.execute(f"""
                update friends
                    set status_id[array_to_string(array_positions(status_id, 2), ',')::int] = 1
                    -- status_id[array_positions(status_id, 2)] = 1
                where user_id={user_active_id}
                    and array_positions(status_id, 0) = array_positions(users_id, {user_passive_id})
            """)
            result = await conn.execute(f"""
                update friends
                    set status_id[array_to_string(array_positions(status_id, 0), ',')::int] = 1
                    -- status_id[array_positions(status_id, 0)] = 1
                where user_id = {user_passive_id}
                    and array_positions(status_id, 2) = array_positions(users_id, {user_active_id})
            """)
        else:
            result = await conn.execute(f"""
                update friends
                    set status_id[array_to_string(array_positions(status_id, 0), ',')::int] = -1
                    --status_id[array_positions(status_id, 0)] = -1
                where user_id = {user_passive_id}
                    and array_positions(status_id, 0) = array_positions(users_id, {user_passive_id})
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
                        select u.user_id, u.name, u.surname, array_to_string(f.status_id, ',')::int as status_id, 
                        img.href
                        from friends as f
                        inner join users_information as u on u.user_id = any(f.users_id)
						left join images as img on img.image_id = u.image_id[array_upper(u.image_id, 1)]
                        where f.user_id = {user_id} and (0 = any(f.status_id) or 2 = any(f.status_id))
                        """)
        return friends
