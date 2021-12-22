import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class SubscribesGetInfo:
    @staticmethod
    async def get_user_subscribes_suggestions(user_id: str, limit=20):
        conn = await asyncpg.connect(connection_url)
        users = await conn.fetch(f"""SELECT u.user_id, u.name, u.surname, img.href
                                     FROM users_information as u 
                                     LEFT JOIN images as img ON img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                     WHERE u.user_id not in (SELECT unnest(users_id) 
                                                       FROM subscribes 
                                                       WHERE user_id = {user_id})
                                     AND u.user_id <> {user_id}
                                     LIMIT {limit}
        """)
        return users

    @staticmethod
    async def get_user_subscribes_suggestion_search(user_id: str, limit=20):
        conn = await asyncpg.connect(connection_url)
        users = await conn.fetch(f"""SELECT u.user_id, u.name, u.surname, img.href
                                     FROM users_information as u 
                                     LEFT JOIN images as img ON img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                     WHERE u.user_id not in (SELECT unnest(users_id) 
                                                       FROM subscribes 
                                                       WHERE user_id = {user_id})
                                     AND u.user_id <> {user_id} AND 
                                     LIMIT {limit}
        """)
        return users

    @staticmethod
    async def get_user_subscribes_names(user_id: str):
        conn = await asyncpg.connect(connection_url)
        users = await conn.fetch(f"""
                SELECT u.user_id, u.name, u.surname, a.href
                FROM users_information as u
                LEFT JOIN images as a
                    ON a.image_id = u.image_id[array_upper(u.image_id, 1)]
                WHERE u.user_id in (SELECT f.users_id[unnest(array_positions(f.status_id, 1))]
                                    FROM subscribes as f
                                    WHERE f.user_id = {user_id})
            """)
        return users

    @staticmethod
    async def get_subscribers(user_id: str):
        conn = await asyncpg.connect(connection_url)
        subscribes = await conn.fetch(f"""
                                            select distinct(u.user_id), u.name, u.surname, f.status_id, f1.status_id as status_id1, img.href
                                            from
                                            (select user_id, unnest(users_id) as users_id, unnest(status_id) as status_id from subscribes) as f
                                            inner join
                                                (select user_id, unnest(users_id) as users_id, unnest(status_id) as status_id from subscribes) as f1 on f1.user_id = f.users_id and f1.users_id = {user_id}
                                            inner join users_information as u on u.user_id = f.users_id
                                            left join images as img on img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                            where f.user_id = {user_id}
            """)
        return subscribes

    @staticmethod
    async def is_block(user_active_id: str,
                       user_passive_id: str):
        conn = await asyncpg.connect(connection_url)
        block = await conn.fetch(f"""
                        select f.status_id
                        from 
                        (select user_id, unnest(users_id) as users_id, unnest(status_id) as status_id from subscribes) as f
                        inner join users_information as u on u.user_id = f.users_id
						left join images as img on img.image_id = u.image_id[array_upper(u.image_id, 1)]
                        where f.user_id = {user_active_id} and u.user_id={user_passive_id}
        """)
        return block


class SubscribesAction:
    @staticmethod
    async def subscribe_user(user_active_id: str, user_passive_id: str):
        conn = await asyncpg.connect(connection_url)
        # тот кто кликает на добавить в друзья,
        # у него 0
        await conn.execute(f"""
            update subscribes
                set users_id = array_append(users_id, {user_passive_id}),
                    status_id = array_append(status_id, 1),
                    last_update = statement_timestamp()
            where user_id = {user_active_id}
        """)
        # тот у кого стоит заявка, у того 2
        await conn.execute(f"""
            update subscribes
                set users_id = array_append(users_id, {user_active_id}),
                    status_id = array_append(status_id, 0),
                    last_update = statement_timestamp()
            where user_id = {user_passive_id}
        """)
        id = await conn.fetch(f""" select max(friend_event_id) from friend_events""")
        id = dict(id[0])['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        await conn.execute(f"""
                        insert INTO friend_events (friend_event_id, user_id_active, user_id_passive,
                                update_date, status_id_active, status_id_passive) values(
                               {id}, '{user_active_id}', '{user_passive_id}', statement_timestamp(), 1, 0)
        """)

    @staticmethod
    async def block_user(user_active_id: str,
                           user_passive_id: str):
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
            update subscribes
                set status_id[array_position(users_id, {user_active_id})] = 2
                where user_id = {user_passive_id}
        """)
        await conn.execute(f"""
            update subscribes
                set status_id[array_position(users_id, {user_passive_id})] = -1
                where user_id = {user_active_id}
        """)
        id = await conn.fetch(f""" select max(friend_event_id) from friend_events""")
        id = dict(id[0])['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        await conn.execute(f"""
                           insert INTO friend_events (friend_event_id, user_id_active, user_id_passive,
                                   update_date,status_id_active, status_id_passive) values(
                                  {id}, '{user_active_id}', '{user_passive_id}', statement_timestamp(), -1, 2)
        """)

    @staticmethod
    async def unsubscribe_user(user_active_id: str, user_passive_id: str):
        #todo if челы подписаны, один отписался чекер
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
                update subscribes
                    set users_id = users_id[:(select array_position(f.users_id, {user_passive_id})
                                    FROM subscribes as f
                                    WHERE f.user_id = {user_active_id})-1] ||
					                users_id[(select array_position(f.users_id, {user_passive_id})
                                    FROM subscribes as f
                                    WHERE f.user_id = {user_active_id})+1:],
                        status_id = status_id[:(select array_position(f.users_id, {user_passive_id})
                                    FROM subscribes as f
                                    WHERE f.user_id = {user_active_id})-1] ||
									status_id[(select array_position(f.users_id, {user_passive_id})
                                    FROM subscribes as f
                                    WHERE f.user_id = {user_active_id})+1:]
                    WHERE user_id = {user_active_id}
        """)
        await conn.execute(f"""
                update subscribes
                    set users_id = users_id[:(select array_position(f.users_id, {user_active_id})
                                FROM subscribes as f
                                WHERE f.user_id = {user_passive_id})-1] ||
					            users_id[(select array_position(f.users_id, {user_active_id})
                                FROM subscribes as f
                                WHERE f.user_id = {user_passive_id})+1:],
                        status_id = status_id[:(select array_position(f.users_id, {user_active_id})
                                FROM subscribes as f
                                WHERE f.user_id = {user_passive_id})-1] ||
					            status_id[(select array_position(f.users_id, {user_active_id})
                                FROM subscribes as f
                                WHERE f.user_id = {user_passive_id})+1:]
                    WHERE user_id = {user_passive_id}
        """)
        id = await conn.fetch(f""" select max(friend_event_id) from friend_events""")
        id = dict(id[0])['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        await conn.execute(f"""
                                   insert INTO friend_events (friend_event_id, user_id_active, user_id_passive,
                                            update_date, status_id_active, status_id_passive) values(
                                            {id}, '{user_active_id}', '{user_passive_id}', statement_timestamp(), 
                                            null, null)
                                    """)

    @staticmethod
    async def unblock_user(user_active_id: str, user_passive_id: str):
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
                        update subscribes
                            set users_id = users_id[:(select array_position(f.users_id, {user_passive_id})
                                            FROM subscribes as f
                                            WHERE f.user_id = {user_active_id})-1] ||
        					                users_id[(select array_position(f.users_id, {user_passive_id})
                                            FROM subscribes as f
                                            WHERE f.user_id = {user_active_id})+1:],
                                status_id = status_id[:(select array_position(f.users_id, {user_passive_id})
                                            FROM subscribes as f
                                            WHERE f.user_id = {user_active_id})-1] ||
        									status_id[(select array_position(f.users_id, {user_passive_id})
                                            FROM subscribes as f
                                            WHERE f.user_id = {user_active_id})+1:]
                            WHERE user_id = {user_active_id}
                """)
        await conn.execute(f"""
                        update subscribes
                            set users_id = users_id[:(select array_position(f.users_id, {user_active_id})
                                        FROM subscribes as f
                                        WHERE f.user_id = {user_passive_id})-1] ||
        					            users_id[(select array_position(f.users_id, {user_active_id})
                                        FROM subscribes as f
                                        WHERE f.user_id = {user_passive_id})+1:],
                                status_id = status_id[:(select array_position(f.users_id, {user_active_id})
                                        FROM subscribes as f
                                        WHERE f.user_id = {user_passive_id})-1] ||
        					            status_id[(select array_position(f.users_id, {user_active_id})
                                        FROM subscribes as f
                                        WHERE f.user_id = {user_passive_id})+1:]
                            WHERE user_id = {user_passive_id}
                """)
        id = await conn.fetch(f""" select max(friend_event_id) from friend_events""")
        id = dict(id[0])['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        await conn.execute(f"""
                                           insert INTO friend_events (friend_event_id, user_id_active, user_id_passive,
                                                    update_date, status_id_active, status_id_passive) values(
                                                    {id}, '{user_active_id}', '{user_passive_id}', statement_timestamp(), 
                                                    null, null)
                                            """)