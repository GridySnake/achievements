import asyncpg
import datetime
from config.common import BaseConfig
connection_url = BaseConfig.database_url
# TODO: change for new db

class Post:
    @staticmethod
    async def create_post(user_id: str,
                          community_id: str,
                          course_id: str,
                          message: str):
        conn = await asyncpg.connect(connection_url)
        post_id = await conn.fetchrow(f"""SELECT MAX(post_id) FROM posts""")
        data = {
            'post_id': int(dict(post_id)['max'])+1,
            'user_id': int(user_id),
            'community_id': int(community_id),
            'course_id': int(course_id),
            'message': message,
            'date_created': datetime.datetime.now()
        }
        await conn.execute(f"""
                        insert INTO posts (post_id, user_id, community_id, course_id, message, date_created) values(
                        {data['post_id']}, {data['user_id']}, {data['community_id']}, {data['course_id']}, '{data['message']}', '{data['date_created']}')
                        """)

    @staticmethod
    async def get_posts_by_user(user_id: str,
                                community_id: str,
                                course_id: str,
                                limit=20):
        conn = await asyncpg.connect(connection_url)
        if user_id:
            posts = await conn.fetch(f"""
                SELECT p.user_id, p.message, , u.last_name, u.first_name
                FROM posts as p
                INNER JOIN users as u ON u.id = p.user_id
                WHERE p.user_id = {user_id}
                LIMIT {limit}
                """)
            return posts
        # if community_id:

