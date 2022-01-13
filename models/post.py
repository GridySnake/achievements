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

        if user_id is None:
            user_id = 'null'
        else:
            user_id = int(user_id)
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
            'user_id': user_id,
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
    async def get_posts_subscribes_me(user_id: str):
        conn = await asyncpg.connect(connection_url)
        posts = await conn.fetch(f"""
                                    select distinct(u.user_id), u.name, u.surname, img1.href as avatar, p.message, p.date_created, img.href
                                    from
                                    (select user_id, unnest(users_id) as users_id, unnest(status_id) as status_id from friends) as f
                                    inner join users_information as u on u.user_id = f.users_id and f.user_id = {user_id} and status_id = 1
                                    left join posts as p on p.user_id = u.user_id
                                    left join images as img on img.image_id = p.image_id
                                    left join images as img1 on img1.image_id = u.image_id[array_upper(u.image_id, 1)]
            """)
        return posts

    @staticmethod
    async def get_posts_by_user(user_id: str,
                                community_id: str = None,
                                course_id: str = None):
        conn = await asyncpg.connect(connection_url)
        if user_id is not None:
            posts = await conn.fetch(f"""
                select p.user_id, p.message, img1.href as avatar,
                        u.name, u.surname, img.href, p.date_created
                from posts as p
                inner join users_information as u 
                    on u.user_id = p.user_id and p.user_id = {user_id}
                left join images as img
                    on img.image_id = p.image_id
                left join images as img1
                    on img1.image_id = u.image_id[array_upper(u.image_id, 1)]
                """)
        elif community_id is not None:
            posts = await conn.fetch(f"""
                select p.community_id, p.message,
                    com.community_name, im.href
                from posts as p
                inner join communities as com
                    on com.community_id = p.community_id
                inner join images as im 
                    on im.image_id = p.image_id
                WHERE p.user_id = {community_id}
            """)
        elif course_id is not None:
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