from datetime import datetime
import asyncpg


class Message:
    @staticmethod
    async def create_message(from_user: str, to_user: str, message: str):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        data = {
            'from_user': from_user,
            'to_user': to_user,
            'message': message,
            'date_created': datetime.now()
        }
        id = await conn.fetchrow(f"""SELECT MAX(message_id) FROM messages""")
        id = int(dict(id)['max']) + 1
        await conn.execute(f"""
                            insert INTO messages (message_id, from_user, to_user, message, date_created) values(
                            {id}, {data['from_user']}, {data['to_user']}, '{data['message']}', '{data['date_created']}')
                            """)

    @staticmethod
    async def get_inbox_messages_by_user(user_id: str, friend, limit=20):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        messages = await conn.fetch(f"""
                            SELECT u.last_name, u.first_name, m.message, m.date_created 
                            FROM messages as m
                            INNER JOIN users as u ON u.id = m.from_user
                            WHERE m.to_user = {user_id} AND m.from_user = {friend}
                            LIMIT {limit}
                            """)
        return messages

    @staticmethod
    async def get_send_messages_by_user(user_id: str, friend, limit=20):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        messages = await conn.fetch(f"""
                                    SELECT u.last_name, u.first_name, m.message, m.date_created 
                                    FROM messages as m
                                    INNER JOIN users as u ON u.id = m.from_user
                                    WHERE m.from_user = {user_id} AND m.to_user = {friend}
                                    LIMIT {limit}
                                    """)
        return messages

    @staticmethod
    async def get_users_chats(user_id: str):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        messages = await conn.fetch(f"""
                                        SELECT distinct(u.id), u.first_name, u.last_name
                                        FROM users as u
                                        LEFT JOIN messages as m ON m.from_user = u.id
											OR m.to_user = u.id
                                        WHERE (m.message_id IN (
                                            SELECT m1.message_id
                                            FROM messages as m1
                                            WHERE m1.to_user = {user_id}
                                            ) 
                                        OR m.message_id IN(
                                            SELECT m2.message_id
                                            FROM messages as m2
                                            WHERE m2.from_user = {user_id}
                                        )) AND u.id <> {user_id}
                                        """)
        return messages

    @staticmethod
    async def get_last_messages(user_id: str, user):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        last_messages = []
        for i in user:
            messages = await conn.fetch(f"""
                                        SELECT m.message, m.date_created, u.first_name, u.last_name
                                        FROM messages as m
                                        LEFT JOIN users as u ON m.from_user = u.id
                                        WHERE (from_user = {i} OR to_user = {i}) AND (from_user = {user_id} OR to_user = {user_id})
                                        ORDER BY date_created DESC
                                        LIMIT 1
                                            """)
            last_messages += messages
        return last_messages


