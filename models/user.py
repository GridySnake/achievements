import hashlib
import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class User:
    @staticmethod
    async def get_user_by_email_phone(email: str, type: str):
        conn = await asyncpg.connect(connection_url)
        user = await conn.fetchrow(f"""
        SELECT * 
        FROM authentication
        WHERE {type} = '{email}' and verified = True
        """)
        user1 = await conn.fetchrow(f"""
                SELECT * 
                FROM authentication
                WHERE {type} = '{email}' and verified = False
                """)
        if user:
            user = dict(user)
            user['id'] = int(user['user_id'])
            return user
        elif user1:
            return 'verify'
        else:
            return dict(error='User with {} {} not found'.format(type, email))

    @staticmethod
    async def get_user_by_id(user_id: str):
        conn = await asyncpg.connect(connection_url)
        user = await conn.fetchrow(f"""
                SELECT *
                FROM users_information
                WHERE user_id = {user_id}
                """)
        if user:
            user = dict(user)
            return user
        else:
            return None

    @staticmethod
    async def get_avatar_by_user_id(user_id: str):
        conn = await asyncpg.connect(connection_url)
        avatar = await conn.fetch(f"""
                SELECT images.href
                FROM images
                INNER JOIN users_information as us ON images.image_id = ANY(us.image_id)
                WHERE us.user_id = {user_id}
                """)
        if avatar:
            return avatar
        else:
            return None

    @staticmethod
    async def create_user_info(data):
        conn = await asyncpg.connect(connection_url)
        result = await conn.execute(f"""
                        UPDATE users_information
                        SET 
                            age = {data['age']},
                            bio = '{data['bio']}',
                            name = '{data['name']}',
                            surname = '{data['surname']}'
                        WHERE user_id = {data['id']}
                        """)

        return result

    @staticmethod
    async def verify_user(href):
        conn = await asyncpg.connect(connection_url)
        verify = await conn.fetchrow(f"""
                            SELECT user_name 
                            FROM authentication
                            WHERE verifying_token = '{href}'
                            """)
        if verify:
            await conn.execute(f"""
                        UPDATE authentication
                        SET verified = True,
                            verifying_token = null
                        WHERE verifying_token = '{href}'
                        """)
        else:
            verify = False
        return verify

    @staticmethod
    async def create_new_user(data, token):
        # TODO: make just phone or email
        email = data['email']
        phone = data['phone']
        conn = await asyncpg.connect(connection_url)
        user = await conn.fetchrow(f"""
                SELECT * 
                FROM authentication
                WHERE email = '{email}' or phone = '{phone}'
                """)
        user_1 = await conn.fetchrow(f"""
                SELECT * 
                FROM authentication
                WHERE (email = '{email}' or phone = '{phone}') and verified <> True
                """)
        if user is not None:
            return dict(error='user with email {} exist'.format(email))

        if user_1 is not None:
            return dict(error='user with email {} exist, but not verified'.format(email))

        if data['user_name'] and data['password'] and (data['phone'] or data['email']):
            data = dict(data)
            data['password'] = hashlib.sha256(data['password'].encode('utf8')).hexdigest()
            id = await conn.fetchrow(f"""SELECT MAX(user_id) FROM users_main""")
            try:
                id = int(dict(id)['max']) + 1
            except:
                id = 0
            if data['email'] and data['phone']:
                None
            elif data['email']:
                data['phone'] = None
            else:
                data['email'] = None
            await conn.execute(f"""
                               insert INTO users_main (user_id, user_name, email, phone) values(
                               {id}, '{data['user_name']}', '{data['email']}', '{data['phone']}')
                               """)
            await conn.execute(f"""
                               insert INTO authentication (email, phone, user_name, password, second_authentication, 
                               user_id, verified, verifying_token) values(
                               '{data['email']}', '{data['phone']}', '{data['user_name']}', '{data['password']}',
                               False, {id}, False, '{token}')
                               """)
            await conn.execute(f"""
                            insert INTO users_information (user_id, country_id, city_id, sex, date_born, age, bio, name, 
                            surname, relation_ship_id, language_id, wedding, communication_conditions, status_work, 
                            position, company_id, school_id, bachelor_id, master_id, image_id, achievements_id) values(
                            {id}, null, null, null, null, null, null, null, null,
                            ARRAY []::integer[], null, null, ARRAY []::text[], null, null, null, null, null, 
                            null, ARRAY []::integer[], ARRAY []::integer[])
                            """)
            await conn.execute(f"""
                                insert INTO user_statistics (user_id, friends, likes, comments, recommendations, 
                                achievements, courses) values(
                                {id}, null, null, null, null, null, null)
                                """)
            await conn.execute(f"""
                                insert INTO user_calendar (user_id, from_date, to_date, free) values(
                                {id}, null, null, null)
                                """)

            result = await conn.execute(f"""
                                        insert INTO friends (relationship_id, user_id, users_id, status_id, last_update) 
                                        values(
                                        {id}, {id}, ARRAY []::integer[], ARRAY []::integer[], null)
                                        """)

            return result
        else:
            return dict(error='Missing user data parameters')

    @staticmethod
    async def save_avatar_url(user_id: str, url: str):
        conn = await asyncpg.connect(connection_url)
        if url is not None and user_id is not None:
            image_id = await conn.fetchrow(f"""SELECT MAX(image_id) FROM images""")
            try:
                image_id = int(dict(image_id)['max']) + 1
            except:
                image_id = 0
            await conn.execute(f"""
                                insert INTO images (image_id, href, image_type, create_date) values(
                                {image_id}, '{url}', 'user', statement_timestamp())
                                """)
            await conn.execute(f"""
                                UPDATE users_information
                                SET image_id = array_append(image_id, {image_id})
                                WHERE user_id = {user_id}
                                """)
            return url
