class MessageGetInfo:
    @staticmethod
    async def get_messages(chat_id: str, conn):
        messages = await conn.fetch(f"""
                                        select u.user_id,  u.surname, u.name, m.message, m.datetime, img.href, 
                                        c.community_id, c.community_name, img1.href as href1, 
                                        c1.course_id, c1.course_name, img2.href as href2, ch.chat_type, ch.participants
                                        from chats as ch
                                        left join messages as m on m.chat_id = ch.chat_id
                                        left join users_information as u on u.user_id = m.from_user and m.from_user_type = 0
                                        left join communities as c on c.community_id = m.from_user and m.from_user_type = 2
                                        left join courses as c1 on c1.course_id = m.from_user and m.from_user_type = 3
                                        left join images as img on img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                        left join images as img1 on img1.image_id = c.image_id[array_upper(u.image_id, 1)]
                                        left join images as img2 on img2.image_id = c1.image_id
                                        where ch.chat_id = {chat_id}
                                        ORDER BY datetime
									""")
        return messages

    @staticmethod
    async def is_owner(chat_id: str, conn):
        owner = await conn.fetchrow(f"""
                                        select u.user_id
                                        from chats as ch
                                        left join communities as c on ch.owner_id = c.community_id and ch.chat_type = 2
                                        left join courses as c1 on ch.owner_id = c1.course_id and ch.chat_type = 3
                                        left join communities as c2 on c2.community_id = c1.course_owner_id and c1.course_owner_type = 1
                                        left join users_information as u on u.user_id = any(c.community_owner_id) or 
                                            u.user_id = c1.course_owner_id and c1.course_owner_type = 0 or u.user_id = any(c2.community_owner_id)
                                        where ch.chat_id = {chat_id}
    								""")
        return owner['user_id']

    @staticmethod
    async def get_chat_owner_cc(chat_id: str, conn):
        owner = await conn.fetchrow(f"""
                                        select ch.owner_id
                                        from chats as ch
                                        where ch.chat_id = {chat_id}
        							""")
        return owner['owner_id']

    # @staticmethod
    # async def get_inbox_messages_by_user(user_id: str, friend, limit=20):
    #     
    #     messages = await conn.fetch(f"""
    #                         SELECT u.user_id, u.surname, u.name, m.message, m.datetime
    #                         FROM messages as m
    #                         INNER JOIN users_information as u ON u.user_id = m.from_user
    #                         WHERE m.to_user = {user_id} AND m.from_user = {friend}
    #                         LIMIT {limit}
    #                         """)
    #     return messages
    #
    # @staticmethod
    # async def get_send_messages_by_user(user_id: str, friend, limit=20):
    #     
    #     messages = await conn.fetch(f"""
    #                                 SELECT u.user_id,  u.surname, u.name, m.message, m.datetime
    #                                 FROM messages as m
    #                                 INNER JOIN users_information as u ON u.user_id = m.from_user
    #                                 WHERE m.from_user = {user_id} AND m.to_user = {friend}
    #                                 LIMIT {limit}
    #                                 """)
    #     return messages

    @staticmethod
    async def get_users_chats(user_id: str, conn):
        chats = await conn.fetch(f"""
                                     select distinct u.user_id, u.name, u.surname, img.href, ch.chat_id, ch.chat_type,
                                        first_value(m.message) over (PARTITION BY m.chat_id order by m.datetime desc) as message,
                                        first_value(m.datetime) over (PARTITION BY m.chat_id order by m.datetime desc) as datetime,
                                        first_value(u1.name) over (PARTITION BY m.chat_id order by m.datetime desc) as m_name,
                                        first_value(u1.surname) over (PARTITION BY m.chat_id order by m.datetime desc) as m_surname,
                                        first_value(m.is_read) over (PARTITION BY m.chat_id order by m.datetime desc) as is_read
                                     from users_information as u
                                     left join (select chat_id, unnest(participants) as participants, chat_type
                                         from chats) as ch on ch.participants = u.user_id and ch.chat_type = 0
                                     left join images as img on img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                     left join messages as m on m.chat_id = ch.chat_id
                                     left join users_information as u1 on m.from_user = u1.user_id
                                     where {user_id} <> ch.participants
                                """)
        return chats

    @staticmethod
    async def get_group_chats(user_id: str, conn):
        chats = await conn.fetch(f"""
                                     select distinct c.group_name, img.href, ch.chat_id, ch.chat_type,
                                        first_value(m.message) over (PARTITION BY m.chat_id order by m.datetime desc) as message,
                                        first_value(m.datetime) over (PARTITION BY m.chat_id order by m.datetime desc) as datetime,
                                        first_value(u.name) over (PARTITION BY m.chat_id order by m.datetime desc) as m_name,
                                        first_value(u.surname) over (PARTITION BY m.chat_id order by m.datetime desc) as m_surname,
                                        first_value(m.is_read) over (PARTITION BY m.chat_id order by m.datetime desc) as is_read
                                     from group_chats_info as c
                                     left join chats as ch on ch.chat_id = c.chat_id and ch.chat_type = 1
                                     left join images as img on img.image_id = c.image_id
                                     left join messages as m on m.chat_id = ch.chat_id
                                     left join users_information as u on m.from_user = u.user_id
                                     where {user_id} = any(ch.participants)
                                """)
        return chats

    @staticmethod
    async def get_community_chats(user_id: str, conn):
        chats = await conn.fetch(f"""
                                    select distinct c.community_id, c.community_name, img.href, ch.chat_id, ch.chat_type,
                                        first_value(m.message) over (PARTITION BY m.chat_id order by m.datetime desc) as message,
                                        first_value(m.datetime) over (PARTITION BY m.chat_id order by m.datetime desc) as datetime,
                                        first_value(u.name) over (PARTITION BY m.chat_id order by m.datetime desc) as m_name,
                                        first_value(u.surname) over (PARTITION BY m.chat_id order by m.datetime desc) as m_surname,
                                        first_value(m.is_read) over (PARTITION BY m.chat_id order by m.datetime desc) as is_read,
                                        first_value(c1.community_name) over (PARTITION BY m.chat_id order by m.datetime desc) as m_community_name
                                    from communities as c
                                    left join chats as ch on ch.owner_id = c.community_id and ch.chat_type = 2
                                    left join images as img on img.image_id = c.image_id[array_upper(c.image_id, 1)]
                                    left join messages as m on m.chat_id = ch.chat_id
                                    left join users_information as u on m.from_user = u.user_id and m.from_user_type = 0
                                    left join communities as c1 on m.from_user = c1.community_id and m.from_user_type = 2
                                    where {user_id} = any(ch.participants)
                                """)
        return chats

    @staticmethod
    async def get_course_chats(user_id: str, conn):
        chats = await conn.fetch(f"""
                                     select distinct c.course_id, c.course_name, img.href, ch.chat_id, ch.chat_type,
                                        first_value(m.message) over (PARTITION BY m.chat_id order by m.datetime desc) as message,
                                        first_value(m.datetime) over (PARTITION BY m.chat_id order by m.datetime desc) as datetime,
                                        first_value(u.name) over (PARTITION BY m.chat_id order by m.datetime desc) as m_name,
                                        first_value(u.surname) over (PARTITION BY m.chat_id order by m.datetime desc) as m_surname,
                                        first_value(m.is_read) over (PARTITION BY m.chat_id order by m.datetime desc) as is_read,
                                        first_value(c1.course_name) over (PARTITION BY m.chat_id order by m.datetime desc) as m_course_name
                                     from courses as c
                                     left join chats as ch on ch.owner_id = c.course_id and ch.chat_type = 3
                                     left join images as img on img.image_id = c.image_id
                                     left join messages as m on m.chat_id = ch.chat_id
                                     left join users_information as u on m.from_user = u.user_id and m.from_user_type = 0
                                     left join courses as c1 on m.from_user = c1.course_id and m.from_user_type = 3
                                     where {user_id} = any(ch.participants)
                                """)
        return chats

    @staticmethod
    async def get_last_messages(chat_id: str, conn):
        last_messages = []
        for i in chat_id:
            messages = await conn.fetch(f"""
                                        SELECT m.message, m.datetime, u.name, u.surname, m.is_read
                                        FROM messages as m
                                        LEFT JOIN users_information as u ON m.from_user = user_id
                                        WHERE m.chat_id = {i}
                                        ORDER BY datetime DESC
                                        limit 1
                                        """)
            last_messages += messages
        return last_messages

    @staticmethod
    async def is_read(user_id: str, chat_id: str, conn):
        await conn.fetch(f"""
                         update messages
                         set is_read = True
                         WHERE from_user <> {user_id} and chat_id = {chat_id}
                        """)

    @staticmethod
    async def get_chat(user_id: str, user_id1: str, conn):
        chat_id = await conn.fetchrow(f"""
                                         select chat_id
                                         from chats
                                         WHERE {user_id} = any(participants) and {user_id1} = any(participants) and chat_type = 0
                                    """)
        if chat_id is None:
            chat_id = -1
        else:
            chat_id = chat_id['chat_id']
        return chat_id

    @staticmethod
    async def get_chat_participants(chat_id: str, user_id: str, conn):
        participants = await conn.fetch(f"""
                                               select u.user_id, u.name, u.surname
                                               from (select chat_id, unnest(participants) as participants from chats) as ch
                                               left join users_information as u on u.user_id = ch.participants
                                               WHERE chat_id = {chat_id} and u.user_id != {user_id}
                                            """)
        return participants


class MessageCreate:
    @staticmethod
    async def create_message(from_user: str, message: str, type1: str, chat_id: str, conn, to_user: str = None):
        message_id = await conn.fetchrow(f"""SELECT MAX(message_id) FROM messages""")
        if dict(message_id)['max'] is not None:
            message_id = int(dict(message_id)['max']) + 1
        else:
            message_id = 0
        if chat_id == -1:
            chat_id = await conn.fetchrow(f"""SELECT MAX(chat_id) FROM chats""")
            if dict(chat_id)['max'] is not None:
                chat_id = int(dict(chat_id)['max']) + 1
            else:
                chat_id = 0
            await conn.execute(f"""
                                    insert INTO chats (chat_id, chat_type, participants, owner_id) values(
                                    {chat_id}, 0, ARRAY[{from_user}, {to_user}], null) 
                                """)

        await conn.execute(f"""
                                insert INTO messages (message_id, from_user, message, from_user_type,
                                datetime, is_read, chat_id) values(
                                {message_id}, {from_user}, '{message}', 
                                {type1}, statement_timestamp(), False, {chat_id})
                            """)

    @staticmethod
    async def create_group_chat(owner_id: str, chat_name: str, conn, chat_avatar: str = None):
        if chat_avatar is None:
            image_id = 'null'
        else:
            image_id = await conn.fetchrow("""select max(image_id) from images""")
            image_id = dict(image_id)['max']
            if image_id is not None:
                image_id += 1
            else:
                image_id = 0
            await conn.execute(f"""
                                    insert into images(image_id, href, image_type, create_date) values(
                                    {image_id}, '{chat_avatar}', 'group', statement_timestamp())
                                """)
        chat_id = await conn.fetchrow("""select max(chat_id) from chats""")
        chat_id = dict(chat_id)['max']
        if chat_id is not None:
            chat_id += 1
        else:
            chat_id = 0
        await conn.execute(f"""
                                insert into chats (chat_id, chat_type, participants, owner_id) values(
                                {chat_id}, 1, array[{owner_id}], {owner_id})
                            """)
        group_id = await conn.fetchrow("""select max(group_id) from group_chats_info""")
        group_id = dict(group_id)['max']
        if group_id is not None:
            group_id += 1
        else:
            group_id = 0
        await conn.execute(f"""
                               insert into group_chats_info (group_id, image_id, group_name, chat_id) values(
                               {group_id}, {image_id}, '{chat_name}', {chat_id})
                            """)
        return chat_id

    @staticmethod
    async def add_member(chat_id: str, users: list, conn):
        await conn.execute(f"""
                               update chats
                                   set participants = array_cat(participants, array[{users}])
                                   where chat_id = {chat_id}
                            """)

    @staticmethod
    async def remove_member(chat_id: str, users: list, conn):
        # todo: заменить цикл
        for i in users:
            await conn.execute(f"""
                                   update chats
                                       set participants = array_remove(participants, {i})
                                       where chat_id = {chat_id}
                                """)
