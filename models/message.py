from datetime import datetime
import asyncpg
from config.common import BaseConfig

connection_url = BaseConfig.database_url


class Message:
    @staticmethod
    async def create_message(from_user: str, to_user: str, message: str, type1: str, type2: str):
        conn = await asyncpg.connect(connection_url)
        data = {
            'from_user': from_user,
            'to_user': to_user,
            'message': message,
            'datetime': datetime.now(),
            'from_user_type': type1,
            'to_user_type': type2
        }
        id = await conn.fetchrow(f"""SELECT MAX(message_id) FROM messages""")
        if dict(id)['max'] is not None:
            id = int(dict(id)['max']) + 1
        else:
            id = 0
        await conn.execute(f"""
                            insert INTO messages (message_id, from_user, to_user, message, from_user_type, to_user_type, 
                            datetime, is_read) values(
                            {id}, {data['from_user']}, {data['to_user']}, '{data['message']}', 
                            '{data['from_user_type']}', 
                            '{data['to_user_type']}', statement_timestamp(), False)
                            """)

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
        messages = await conn.fetch(f"""
                                        SELECT distinct(u.user_id), u.name, u.surname, img.href
                                        FROM users_information as u
                                        LEFT JOIN messages as m ON m.from_user = u.user_id
										    OR m.to_user = u.user_id
                                        LEFT JOIN images as img ON img.image_id = u.image_id[array_upper(u.image_id, 1)]
                                        WHERE (m.message_id IN (
                                            SELECT m1.message_id
                                            FROM messages as m1
                                            WHERE m1.to_user = {user_id}
                                            ) 
                                        OR m.message_id IN(
                                            SELECT m2.message_id
                                            FROM messages as m2
                                            WHERE m2.from_user = {user_id}
                                        )) AND u.user_id <> {user_id}
                                        """)
        return messages

    @staticmethod
    async def get_last_messages(user_id: str, user):
        conn = await asyncpg.connect(connection_url)
        last_messages = []
        for i in user:
            messages = await conn.fetch(f"""
                                        SELECT m.message, m.datetime, u.name, u.surname
                                        FROM messages as m
                                        LEFT JOIN users_information as u ON m.from_user = user_id
                                        WHERE (from_user = {i} OR to_user = {i}) AND (from_user = {user_id} 
                                        OR to_user = {user_id})
                                        ORDER BY datetime DESC
                                        LIMIT 1
                                        """)
            last_messages += messages
        return last_messages
