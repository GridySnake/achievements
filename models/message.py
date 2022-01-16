from datetime import datetime
import asyncpg
from config.common import BaseConfig

connection_url = BaseConfig.database_url


class MessageGetInfo:
    @staticmethod
    async def get_messages(user_id: str, friend):
        conn = await asyncpg.connect(connection_url)
        messages = await conn.fetch(f"""
                                    SELECT u.user_id,  u.surname, u.name, m.message, m.datetime, img.href
                                    FROM messages as m
                                    INNER JOIN users_information as u ON u.user_id = m.from_user
                                    LEFT JOIN images as img ON img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                    WHERE (m.message_id IN (
									SELECT message_id 
									FROM messages
									WHERE messages.from_user = {user_id} AND messages.to_user = {friend}
									) OR (m.message_id IN (
									SELECT message_id 
									FROM messages
									WHERE messages.from_user = {friend} AND messages.to_user = {user_id})))
									ORDER BY datetime
									""")
        return messages

    @staticmethod
    async def get_inbox_messages_by_user(user_id: str, friend, limit=20):
        conn = await asyncpg.connect(connection_url)
        messages = await conn.fetch(f"""
                            SELECT u.user_id, u.surname, u.name, m.message, m.datetime 
                            FROM messages as m
                            INNER JOIN users_information as u ON u.user_id = m.from_user
                            WHERE m.to_user = {user_id} AND m.from_user = {friend}
                            LIMIT {limit}
                            """)
        return messages

    @staticmethod
    async def get_send_messages_by_user(user_id: str, friend, limit=20):
        conn = await asyncpg.connect(connection_url)
        messages = await conn.fetch(f"""
                                    SELECT u.user_id,  u.surname, u.name, m.message, m.datetime 
                                    FROM messages as m
                                    INNER JOIN users_information as u ON u.user_id = m.from_user
                                    WHERE m.from_user = {user_id} AND m.to_user = {friend}
                                    LIMIT {limit}
                                    """)
        return messages

    @staticmethod
    async def get_users_chats(user_id: str):
        conn = await asyncpg.connect(connection_url)
        chats = await conn.fetch(f"""
                                     select distinct u.user_id, u.name, u.surname, img.href, ch.chat_id, ch.chat_type
                                     from users_information as u
                                     left join (select chat_id, unnest(participants) as participants, chat_type 
                                         from chats) as ch on ch.participants = u.user_id and ch.chat_type = 0
                                     left join images as img on img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                     where {user_id} <> ch.participants
                                """)
        return chats

    # todo: group chats

    @staticmethod
    async def get_community_chats(user_id: str):
        conn = await asyncpg.connect(connection_url)
        chats = await conn.fetch(f"""
                                        select distinct c.community_id, c.community_name, img.href, ch.chat_id, ch.chat_type
                                        from communities as c
                                        left join chats as ch on ch.owner_id = c.community_id and ch.chat_type = 2
                                        left join images as img on img.image_id = c.image_id[array_upper(c.image_id, 1)]
                                        where {user_id} = any(ch.participants)
                                    """)
        return chats

    @staticmethod
    async def get_course_chats(user_id: str):
        conn = await asyncpg.connect(connection_url)
        chats = await conn.fetch(f"""
                                     select distinct c.course_id, c.course_name, img.href, ch.chat_id, ch.chat_type
                                     from courses as c
                                     left join chats as ch on ch.owner_id = c.course_id and ch.chat_type = 3
                                     left join images as img on img.image_id = c.image_id
                                     where {user_id} = any(ch.participants)
                                """)
        return chats

    @staticmethod
    async def get_last_messages(user_id: str, user):
        conn = await asyncpg.connect(connection_url)
        last_messages = []
        for i in user:
            messages = await conn.fetch(f"""
                                        SELECT m.message, m.datetime, u.name, u.surname, m.is_read
                                        FROM messages as m
                                        LEFT JOIN users_information as u ON m.from_user = user_id
                                        WHERE (from_user = {i} OR to_user = {i}) AND (from_user = {user_id} 
                                        OR to_user = {user_id})
                                        ORDER BY datetime DESC
                                        """)
            last_messages += messages
        return last_messages

    @staticmethod
    async def is_read(user_id: str, chat_id: str):
        conn = await asyncpg.connect(connection_url)
        await conn.fetch(f"""
                         update messages
                         set is_read = True
                         WHERE from_user = {chat_id} and to_user = {user_id}
                        """)


class MessageCreate:
    @staticmethod
    async def create_message(from_user: str, to_user: str, message: str, type1: str, type2: str, chat_id: str):
        # todo: chat_type
        conn = await asyncpg.connect(connection_url)
        data = {
            'from_user': from_user,
            'to_user': to_user,
            'message': message,
            'datetime': datetime.now(),
            'from_user_type': type1,
            'to_user_type': type2,
            'chat_id': chat_id
        }
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
                                insert INTO messages (message_id, from_user, to_user, message, from_user_type, to_user_type,
                                datetime, is_read, chat_id) values(
                                {message_id}, {data['from_user']}, {data['to_user']}, '{data['message']}', 
                                '{data['from_user_type']}', 
                                '{data['to_user_type']}', statement_timestamp(), False, {chat_id})
                            """)