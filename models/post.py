import asyncpg
import datetime
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class Post:
    @staticmethod
    async def create_post(user_id: str,
                          message: str,
                          image_href: str = None,
                          community_id: str = None,
                          course_id: str = None):
        conn = await asyncpg.connect(connection_url)
        post_id = await conn.fetchrow(f"""SELECT MAX(post_id) FROM posts""")
        if post_id['max'] is not None:
            post_id = int(post_id['max']) + 1
        else:
            post_id = 0
        if community_id is None:
            community_id = 'null'
        else:
            community_id = int(community_id)
        if course_id is None:
            course_id = 'null'
        else:
            course_id = int(course_id)
        if image_href is None:
            image_id = 'null'
        else:
            image_id = await conn.fetchrow(f"""SELECT MAX(image_id) FROM images""")
            try:
                image_id = int(dict(image_id)['max']) + 1
            except:
                image_id = 0
            await conn.execute(f"""
                               insert INTO images (image_id, href, image_type, create_date) values(
                               {image_id}, '{image_href}', 'user_post', statement_timestamp())
            """)
        data = {
            'post_id': post_id,
            'user_id': int(user_id),
            'community_id': community_id,
            'course_id': course_id,
            'message': message,
            'date_created': datetime.datetime.now(),
            'image_id': image_id
        }

        await conn.execute(f"""
                        insert INTO posts (post_id, user_id, community_id, course_id, message, image_id, date_created) 
                        values(
                        {data['post_id']}, {data['user_id']}, {data['community_id']}, {data['course_id']}, 
                        '{data['message']}', {data['image_id']}, statement_timestamp())
        """)

    @staticmethod
    async def get_posts_by_user(user_id: str,
                                community_id: str = None,
                                course_id: str = None,
                                limit=20):
        conn = await asyncpg.connect(connection_url)
        if user_id:
            posts = await conn.fetch(f"""
                SELECT p.user_id, p.message, im.href,
                        u.name, u.surname, im.href, p.date_created
                FROM posts as p
                INNER JOIN users_information as u 
                    ON u.user_id = p.user_id
                LEFT JOIN images as im 
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
