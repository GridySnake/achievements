import asyncpg
import datetime


class Post:

    @staticmethod
    async def create_post(user_id: str, message: str):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        post_id = await conn.fetchrow(f"""SELECT MAX(post_id) FROM posts""")
        data = {
            'post_id': int(dict(post_id)['max'])+1,
            'user_id': int(user_id),
            'message': message,
            'date_created': datetime.datetime.now()
        }
        await conn.execute(f"""
                        insert INTO posts (post_id, user_id, message, date_created) values(
                        {data['post_id']}, {data['user_id']}, '{data['message']}', '{data['date_created']}')
                        """)

    @staticmethod
    async def get_posts_by_user(user_id: str, limit=20):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        posts = await conn.fetch(f"""
            SELECT p.*, u.last_name, u.first_name
            FROM posts as p
            INNER JOIN users as u ON u.id = p.user_id
            WHERE p.user_id = {user_id}
            LIMIT {limit}
            """)
        return posts
