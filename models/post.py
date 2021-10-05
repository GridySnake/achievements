import asyncpg
import datetime
from config.common import BaseConfig
connection_url = BaseConfig.database_url

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
                        {data['post_id']}, {data['user_id']}, {data['community_id']}, {data['course_id']}, 
                        '{data['message']}', '{data['date_created']}')
                        """)

    @staticmethod
    async def get_posts_by_user(user_id: str,
                                community_id: str,
                                course_id: str,
                                limit=20):
        conn = await asyncpg.connect(connection_url)
        if user_id:
            posts = await conn.fetch(f"""
                SELECT p.user_id, p.message, 
                        u.name, u.surname, im.href
                FROM posts as p
                INNER JOIN users_information as u 
                    ON u.user_id = p.user_id
                INNER JOIN images as im 
                    on im.image_id = p.image_id
                WHERE p.user_id = {user_id}
                LIMIT {limit}
                """)
            return posts
        if community_id:
            posts = await conn.fetch(f"""
                select p.community_id, p.message,
                    com.community_name, im.href
                from posts as p
                inner join communities as com
                    on com.community_id = p.community_id
                inner join images as im 
                    on im.image_id = p.image_id
                WHERE p.user_id = {community_id}
                LIMIT {limit}
            """)
            return posts
        if course_id:
            posts = await conn.fetch(f"""
                select p.course_id, p.message,
                    cour.course_name, im.href
                from posts as p
                inner join courses as cour
                    on cour.course_id = p.course_id
                inner join images as im 
                    on im.image_id = p.image_id
                WHERE p.user_id = {course_id}
            """)
            return posts
