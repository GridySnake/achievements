import hashlib
import asyncpgsa
from config.common import BaseConfig
import asyncpg
from asyncpgsa import pg
database = asyncpgsa.create_pool(
        host=BaseConfig.host,
        port=BaseConfig.port,
        database=BaseConfig.database_name,
        user=BaseConfig.user,
        password=BaseConfig.password
    )


class User:
    @staticmethod
    async def get_user_by_email_phone(email: str, type: str):
        conn = await asyncpg.connect('postgresql://gachi_achi:achi_for_gachi@204.2.63.15:10485/achievements')
        user = await conn.fetchrow(f"""
        SELECT * 
        FROM authentication
        WHERE {type} = '{email}'
        """)
        user = dict(user)
        if user:
            user['id'] = int(user['user_id'])
            #user['friends'] = [str(uid) for uid in user['friends']]
            return user
        else:
            return dict(error='User with {} {} not found'.format(type, email))

    @staticmethod
    async def get_user_by_id(user_id: str):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        user = await conn.fetchrow(f"""
                SELECT users.*, avatars.url
                FROM users
                LEFT JOIN avatars ON avatars.user_id = users.id
                WHERE id = '{user_id}'
                """)
        # friends = await conn.fetchrow(f"""SELECT u.*
        #                              FROM users as u
        #                              WHERE u.id in (SELECT unnest(friend)
        #                                                FROM friends
        #                                                WHERE user_id = {user_id})
        #                              AND u.id <> {user_id}
        #         """)
        user = dict(user)
        #friends = dict(friends)
        if user:
            user['id'] = int(user['id'])
            #user['friends'] = [str(uid) for uid in friends['friend']]
            return user
        else:
            return None

    @staticmethod
    async def create_user_info(data):
        conn = await asyncpg.connect('postgresql://gachi_achi:achi_for_gachi@204.2.63.15:10485/achievements')
        id = await conn.fetchrow(f"""SELECT MAX(user_id) FROM user_main""")
        id = int(dict(id)['max']) + 1
        if id:
            id = id
        else:
            id = 0
        await conn.execute(f"""
                        insert INTO user_information (user_id, country_id, city_id, sex, date_born, age, bio, name, 
                        surname, relation_ship_id, language_id, wedding, communication_conditions, status_work, 
                        position, company_id, school_id, bachelor_id, master_id, image_id) values(
                        {id}, null, null, null, null, null, null, null, null,
                        ARRAY []::integer[], null, null, ARRAY []::text[], null, null, null, null, null, 
                        null, ARRAY []::integer[])
                        """)
        await conn.execute(f"""
                                insert INTO authentication (email, phone, user_name, password, second_authentication) 
                                values(
                                '{data['email']}', '{data['phone']}', '{data['user_name']}', '{data['password']}',
                                False, {id})
                                """)
        result = await conn.execute(f"""
                                insert INTO users_main (user_id, user_name, email, phone) values(
                                {id}, '{data['user_name']}', '{data['email']}', '{data['phone']}')
                                """)
        return result

    @staticmethod
    async def create_new_user(data):
        email = data['email']
        phone = data['phone']
        conn = await asyncpg.connect('postgresql://gachi_achi:achi_for_gachi@204.2.63.15:10485/achievements')
        user = await conn.fetchrow(f"""
                SELECT * 
                FROM authentication
                WHERE email = '{email}' or phone = '{phone}'
                """)
        if user is not None:
            return dict(error='user with email {} exist'.format(email))

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
                               insert INTO authentication (email, phone, user_name, password, second_authentication, user_id) 
                               values(
                               '{data['email']}', '{data['phone']}', '{data['user_name']}', '{data['password']}',
                               False, {id})
                               """)
            result = await conn.execute(f"""
                            insert INTO users_information (user_id, country_id, city_id, sex, date_born, age, bio, name, 
                            surname, relation_ship_id, language_id, wedding, communication_conditions, status_work, 
                            position, company_id, school_id, bachelor_id, master_id, image_id) values(
                            {id}, null, null, null, null, null, null, null, null,
                            ARRAY []::integer[], null, null, ARRAY []::text[], null, null, null, null, null, 
                            null, ARRAY []::integer[])
                            """)


            return result
        else:
            return dict(error='Missing user data parameters')

    @staticmethod
    async def save_avatar_url(user_id: str, url: str):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        if url is not None and user_id is not None:
            us_id = await conn.fetchrow(f"""SELECT user_id FROM avatars WHERE user_id = {user_id}""")
            #url = 'C:/Users/kunil/PycharmProjects/social-network/static/avatars/' + url
            if us_id is None:
                avatar_id = await conn.fetchrow(f"""SELECT MAX(avatar_id) FROM avatars""")
                avatar_id = int(dict(avatar_id)['max']) + 1
                await conn.execute(f"""
                                insert INTO avatars (avatar_id, user_id, url) values(
                                {avatar_id}, {user_id}, '{url}')
                                """)
            else:
                await conn.execute(f"""
                                                UPDATE avatars 
                                                SET url = '{url}' 
                                                WHERE user_id = {user_id}
                                                """)
            return url

    @staticmethod
    async def get_user_friends_suggestions(user_id: str, limit=20):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        users = await conn.fetch(f"""SELECT u.* 
                                     FROM users as u 
                                     WHERE u.id not in (SELECT unnest(friend) 
                                                       FROM friends 
                                                       WHERE user_id = {user_id})
                                     AND u.id <> {user_id}
                                     LIMIT {limit}
        """)
        return users

    @staticmethod
    async def get_user_friends_names(user_id: str, limit=20):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        users = await conn.fetch(f"""SELECT u.id, u.first_name, u.last_name, a.url
                                     FROM users as u 
                                     LEFT JOIN avatars as a ON a.user_id = u.id
                                     WHERE u.id in (SELECT unnest(f.friend) 
                                                       FROM friends as f
                                                       WHERE f.user_id = {user_id})
                                     LIMIT {limit}
        """)
        return users

    @staticmethod
    async def get_user_friends(user_id: str, limit=20):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        user_friends = await conn.fetchrow(f"""SELECT friend FROM friends WHERE user_id = {user_id} LIMIT {limit}""")
        return user_friends

    @staticmethod
    async def add_friend(user_id: str, friend_id: str):
        conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
        friends = User.get_user_friends(user_id)
        if friends is not None:
            friends = await conn.fetchrow(f"""SELECT friend FROM friends WHERE user_id = {user_id} AND {friend_id} = ANY(friend)""")
            if friends is not None:
                pass
            else:
                await conn.execute(
                f"""UPDATE friends
                    SET friend = array_append(friend, {friend_id})
                    WHERE user_id = {user_id}
                   """)
        else:
            await conn.execute(
                f"""insert INTO friends (user_id, friend) values(
           {user_id}, ARRAY[{friend_id}])
""")
