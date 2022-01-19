import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class SubscribesGetInfo:
    """
    Class for getting information for subscribes
    ...
    Attributes
    ----------
    None

    Methods
    -------
    get_user_subscribes_suggestions(user_id: str)
        Give users witch have no connection to user
    get_user_subscribes_names(user_id: str)
        Give information about subscribers
    get_subscribers(user_id: str)
        Give list of active and passive subscribers
    is_block(user_active_id: str, user_passive_id: str)
        Give status of follower
    """
    @staticmethod
    async def get_user_subscribes_suggestions(user_id: str):
        """
        :param user_id: str
        :return: list of asyncpg records: user_id, name, surname, href
        """
        conn = await asyncpg.connect(connection_url)
        users = await conn.fetch(f"""select u.user_id, u.name, u.surname, img.href
                                     from users_information as u 
                                     left join images as img on img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                     where u.user_id not in (select unnest(users_id) 
                                                       from subscribes 
                                                       where user_id = {user_id})
                                     and u.user_id <> {user_id}
        """)
        return users

    @staticmethod
    async def get_user_subscribes_names(user_id: str):
        """
        :param user_id: str
        :return: list of asyncpg records: user_id, name, surname, href
        """
        conn = await asyncpg.connect(connection_url)
        users = await conn.fetch(f"""
                select u.user_id, u.name, u.surname, a.href
                from users_information as u
                left join images as a
                    on a.image_id = u.image_id[array_upper(u.image_id, 1)]
                where u.user_id in (select f.users_id[unnest(array_positions(f.status_id, 1))]
                                    from subscribes as f
                                    where f.user_id = {user_id})
            """)
        return users

    @staticmethod
    async def get_subscribers(user_id: str):
        """
        :param user_id: str
        :return: list of asyncpg records: user_id, name, surname, status_active, status_passive, href
        """
        conn = await asyncpg.connect(connection_url)
        subscribes = await conn.fetch(f"""
                                          select distinct(u.user_id), u.name, u.surname, f.status_id as status_active, f1.status_id as status_passive, img.href
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
    async def is_block(user_active_id: str, user_passive_id: str):
        """
        :param user_active_id: str
        :param user_passive_id: str
        :return: asyncpg record: status_id
        """
        conn = await asyncpg.connect(connection_url)
        block = await conn.fetchrow(f"""
                        select case when f.status_id = 2 then true
                                else false
                                end as block
                        from 
                        (select user_id, unnest(users_id) as users_id, unnest(status_id) as status_id from subscribes) as f
                        inner join users_information as u on u.user_id = f.users_id
                        where f.user_id = {user_active_id} and u.user_id={user_passive_id}
        """)
        return block['block']


class SubscribesAction:
    """
    Class for make actions for subscribes (follow, unfollow, block, unblock)
    ...
    Attributes
    ----------
    None

    Methods
    -------
    subscribe_user(user_active_id: str, user_passive_id: str)
        Subscribe user
    block_user(user_active_id: str, user_passive_id: str)
        Block user
    unsubscribe_user(user_active_id: str, user_passive_id: str)
        Unsubscribe user which user has been followed
    unblock_user(user_active_id: str, user_passive_id: str)
        Unblock user which user has been blocked
    """
    @staticmethod
    async def subscribe_user(user_active_id: str, user_passive_id: str):
        """
        :param user_active_id: str
        :param user_passive_id: str
        :return: None
        """
        conn = await asyncpg.connect(connection_url)
        checker = await conn.fetchrow(f"""
                                          select
                                          status_id[(select array_position(f.users_id, {user_passive_id})
                                          from subscribes as f
                                          where f.user_id = {user_active_id})::int]
                                          from subscribes
                                          where user_id = {user_active_id}
                                          """)
        checker = dict(checker)['status_id']
        id = await conn.fetchrow(f""" select max(friend_event_id) from friend_events""")
        id = dict(id)['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        if checker is None:
            await conn.execute(f"""
                update subscribes
                    set users_id = array_append(users_id, {user_passive_id}),
                        status_id = array_append(status_id, 1),
                        last_update = statement_timestamp()
                where user_id = {user_active_id}
            """)
            await conn.execute(f"""
                        update subscribes
                            set users_id = array_append(users_id, {user_active_id}),
                                status_id = array_append(status_id, 0),
                                last_update = statement_timestamp()
                        where user_id = {user_passive_id}
                    """)
            await conn.execute(f"""
                                    insert into friend_events (friend_event_id, user_id_active, user_id_passive,
                                    update_date, status_id_active, status_id_passive) values(
                                    {id}, '{user_active_id}', '{user_passive_id}', statement_timestamp(), 1, 0)
                    """)
        else:
            await conn.execute(f"""
                                    update subscribes
                                        set status_id[(select array_position(f.users_id, {user_passive_id})
                                                    from subscribes as f
                                                    where f.user_id = {user_active_id})] = 1
                                        where user_id = {user_active_id}
                                    """)
            await conn.execute(f"""
                                    insert into friend_events (friend_event_id, user_id_active, user_id_passive,
                                    update_date, status_id_active, status_id_passive) values(
                                    {id}, '{user_active_id}', '{user_passive_id}', statement_timestamp(), 1, 1)
                    """)

    @staticmethod
    async def block_user(user_active_id: str, user_passive_id: str):
        """
        :param user_active_id: str
        :param user_passive_id: str
        :return: None
        """
        conn = await asyncpg.connect(connection_url)
        checker = await conn.fetchrow(f"""
                                          select
                                          status_id[(select array_position(f.users_id, {user_passive_id})
                                          from subscribes as f
                                          where f.user_id = {user_active_id})::int]
                                          from subscribes
                                          where user_id = {user_active_id}
                                          """)
        checker = dict(checker)['status_id']
        if checker is not None:
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
        else:
            await conn.execute(f"""
                                    update subscribes
                                        set users_id = array_append(users_id, {user_passive_id}),
                                            status_id = array_append(status_id, -1),
                                            last_update = statement_timestamp()
                                    where user_id = {user_active_id}
                                """)
            await conn.execute(f"""
                                   update subscribes
                                       set users_id = array_append(users_id, {user_active_id}),
                                           status_id = array_append(status_id, 2),
                                           last_update = statement_timestamp()
                                   where user_id = {user_passive_id}
                                    """)

        id = await conn.fetchrow(f""" select max(friend_event_id) from friend_events""")
        id = dict(id)['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        await conn.execute(f"""
                           insert into friend_events (friend_event_id, user_id_active, user_id_passive,
                           update_date,status_id_active, status_id_passive) values(
                           {id}, '{user_active_id}', '{user_passive_id}', statement_timestamp(), -1, 2)
        """)

    @staticmethod
    async def unsubscribe_user(user_active_id: str, user_passive_id: str):
        """
        :param user_active_id: str
        :param user_passive_id: str
        :return: None
        """
        conn = await asyncpg.connect(connection_url)
        checker = await conn.fetchrow(f"""
                                          select
                                          status_id[(select array_position(f.users_id, {user_active_id})
                                          from subscribes as f
                                          where f.user_id = {user_passive_id})::int]
                                          from subscribes
                                          where user_id = {user_passive_id}
                                              """)
        checker = dict(checker)['status_id']
        if checker == 1:
            await conn.execute(f"""
                                update subscribes
                                    set status_id[(select array_position(f.users_id, {user_passive_id})
                                                from subscribes as f
                                                where f.user_id = {user_active_id})] = 0
                                    where user_id = {user_active_id}
                        """)
        else:
            await conn.execute(f"""
                    update subscribes
                        set users_id = users_id[:(select array_position(f.users_id, {user_passive_id})
                                        from subscribes as f
                                        where f.user_id = {user_active_id})-1] ||
                                        users_id[(select array_position(f.users_id, {user_passive_id})
                                        from subscribes as f
                                        where f.user_id = {user_active_id})+1:],
                            status_id = status_id[:(select array_position(f.users_id, {user_passive_id})
                                        from subscribes as f
                                        where f.user_id = {user_active_id})-1] ||
                                        status_id[(select array_position(f.users_id, {user_passive_id})
                                        from subscribes as f
                                        where f.user_id = {user_active_id})+1:]
                        where user_id = {user_active_id}
            """)

            await conn.execute(f"""
                    update subscribes
                        set users_id = users_id[:(select array_position(f.users_id, {user_active_id})
                                    from subscribes as f
                                    where f.user_id = {user_passive_id})-1] ||
                                    users_id[(select array_position(f.users_id, {user_active_id})
                                    from subscribes as f
                                    where f.user_id = {user_passive_id})+1:],
                            status_id = status_id[:(select array_position(f.users_id, {user_active_id})
                                    from subscribes as f
                                    where f.user_id = {user_passive_id})-1] ||
                                    status_id[(select array_position(f.users_id, {user_active_id})
                                    from subscribes as f
                                    where f.user_id = {user_passive_id})+1:]
                        where user_id = {user_passive_id}
            """)

        id = await conn.fetchrow(f""" select max(friend_event_id) from friend_events""")
        id = dict(id)['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        await conn.execute(f"""
                               insert into friend_events (friend_event_id, user_id_active, user_id_passive,
                               update_date, status_id_active, status_id_passive) values(
                               {id}, '{user_active_id}', '{user_passive_id}', statement_timestamp(), 
                               0, {checker})
                                """)

    @staticmethod
    async def unblock_user(user_active_id: str, user_passive_id: str):
        """
        :param user_active_id: str
        :param user_passive_id: str
        :return: None
        """
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
                        update subscribes
                            set users_id = users_id[:(select array_position(f.users_id, {user_passive_id})
                                            from subscribes as f
                                            where f.user_id = {user_active_id})-1] ||
        					                users_id[(select array_position(f.users_id, {user_passive_id})
                                            from subscribes as f
                                            where f.user_id = {user_active_id})+1:],
                                status_id = status_id[:(select array_position(f.users_id, {user_passive_id})
                                            from subscribes as f
                                            where f.user_id = {user_active_id})-1] ||
        									status_id[(select array_position(f.users_id, {user_passive_id})
                                            from subscribes as f
                                            where f.user_id = {user_active_id})+1:]
                            where user_id = {user_active_id}
                """)
        await conn.execute(f"""
                        update subscribes
                            set users_id = users_id[:(select array_position(f.users_id, {user_active_id})
                                        from subscribes as f
                                        where f.user_id = {user_passive_id})-1] ||
        					            users_id[(select array_position(f.users_id, {user_active_id})
                                        from subscribes as f
                                        where f.user_id = {user_passive_id})+1:],
                                status_id = status_id[:(select array_position(f.users_id, {user_active_id})
                                        from subscribes as f
                                        where f.user_id = {user_passive_id})-1] ||
        					            status_id[(select array_position(f.users_id, {user_active_id})
                                        from subscribes as f
                                        where f.user_id = {user_passive_id})+1:]
                            where user_id = {user_passive_id}
                """)
        id = await conn.fetchrow(f""" select max(friend_event_id) from friend_events""")
        id = dict(id)['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        await conn.execute(f"""
                               insert into friend_events (friend_event_id, user_id_active, user_id_passive,
                               update_date, status_id_active, status_id_passive) values(
                               {id}, '{user_active_id}', '{user_passive_id}', statement_timestamp(), 
                               0, 0)
                            """)
