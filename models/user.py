import hashlib
import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class UserGetInfo:
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
    async def get_user_info_by_value(user_id: str, value: str):
        conn = await asyncpg.connect(connection_url)
        user = await conn.fetchrow(f"""
                    select {value}
                    from users_information
                    where user_id = {user_id}
                    """)
        return user[value]

    @staticmethod
    async def get_user_info(user_id: str):
        conn = await asyncpg.connect(connection_url)
        user = await conn.fetchrow(f"""
                            select name, surname, c.country_name_native, c.country_id, age, bio
                            from users_information as ui
                            left join countries as c on c.country_id = ui.country_id
                            where user_id = {user_id}
                            """)
        return user

    @staticmethod
    async def get_user_info_by_count(user_id: str, value: str):
        conn = await asyncpg.connect(connection_url)
        course = await conn.fetchrow(f"""
                                      select {value} 
                                      from user_statistics
                                      where user_id = {user_id}
                                    """)
        return course[value]

    @staticmethod
    async def get_avatar_by_user_id(user_id: str):
        conn = await asyncpg.connect(connection_url)
        avatar = await conn.fetch(f"""
                SELECT images.href
                FROM images
                INNER JOIN users_information as us ON images.image_id = ANY(us.image_id) and images.image_type = 'user'
                WHERE us.user_id = {user_id}
                """)
        if avatar:
            return avatar
        else:
            return None

    @staticmethod
    async def check_connect(user_id: str, service_id: str):
        conn = await asyncpg.connect(connection_url)
        count = await conn.fetchrow(f"""select count(services_id)
                                    from users_information
                                    where user_id = {user_id} and {service_id} in (select unnest(services_id) from users_information where user_id={user_id})
        """)
        if count['count'] > 0:
            return True
        else:
            return False

    @staticmethod
    async def get_user_name_by_service(user_id: str, service_id: str):
        conn = await asyncpg.connect(connection_url)
        username = await conn.fetchrow(f"""select services_username
                                        from users_information
                                        where user_id = {user_id} and {service_id} in (select unnest(services_id) from users_information where user_id={user_id})
        """)
        return username


class UserCreate:
    @staticmethod
    async def create_user_info(user_id: str, data: dict):
        conn = await asyncpg.connect(connection_url)
        for i in data.keys():
            await conn.execute(f"""
                                    update users_information
                                    set 
                                        {i} = '{data[i]}'
                                    where user_id = {user_id}
                            """)

    @staticmethod
    async def get_user_info(user_id: str):
        conn = await asyncpg.connect(connection_url)
        user_info = await conn.fetchrow(f"""
                                            select name, surname, bio, birthday
                                            from users_information
                                            where user_id = {user_id}
                                        """)
        return user_info

    @staticmethod
    async def create_user_info_conditions(user_id: str, data: dict):
        conn = await asyncpg.connect(connection_url)
        for i in range(len(data['condition_id'])):
            condition_id = await conn.fetchrow("select max(condition_id) from conditions")
            condition_id = dict(condition_id)['max']
            if condition_id is not None:
                condition_id += 1
            else:
                condition_id = 0
            if data['task'][i] != 'null' and data['answers'][i] == 'null' and data['condition_value'][i] != 'null' \
                    and data['images'][i] == 'null':
                await conn.execute(f"""
                                       insert into conditions (condition_id, task, answer, condition_value, image_id, 
                                           generate_condition_id)
                                           values ({condition_id}, '{data['task'][i]}', {data['answers'][i]},
                                           '{data['condition_value'][i]}', null, {data['condition_id'][i]})
                                    """)
            elif data['task'][i] == 'null' and data['condition_value'][i] != 'null':
                await conn.execute(f"""
                                       insert into conditions (condition_id, task, answer, condition_value, image_id, 
                                           generate_condition_id)
                                           values ({condition_id}, {data['task'][i]}, {data['answers'][i]},
                                           '{data['condition_value'][i]}', null, {data['condition_id'][i]})
                                    """)
            elif data['task'][i] == 'null' and data['condition_value'][i] == 'null':
                await conn.execute(f"""
                                       insert into conditions (condition_id, task, answer, condition_value, image_id, 
                                           generate_condition_id)
                                           values ({condition_id}, {data['task'][i]}, {data['answers'][i]},
                                           {data['condition_value'][i]}, null, {data['condition_id'][i]})
                                    """)
            elif data['task'][i] != 'null' and data['answers'][i] != 'null' and data['condition_value'][i] != 'null' \
                    and data['images'][i] == 'null':
                await conn.execute(f"""
                                       insert into conditions (condition_id, task, answer, condition_value, image_id, 
                                           generate_condition_id)
                                           values ({condition_id}, '{data['task'][i]}', '{data['answers'][i]}',
                                           '{data['condition_value'][i]}', null, {data['condition_id'][i]})
                                    """)
            else:
                image_id = await conn.fetchrow("select max(image_id) from images")
                image_id = dict(image_id)['max']
                if image_id is not None:
                    image_id += 1
                else:
                    image_id = 0
                await conn.execute(f"""
                                        insert into images (image_id, href, image_type, create_date) 
                                            values ({image_id}, '{data['images'][i]}', 1, statement_timestamp())
                                    """)
                await conn.execute(f"""
                                        insert into conditions (condition_id, task, answer, condition_value, image_id, 
                                            generate_condition_id)
                                            values ({condition_id}, '{data['task'][i]}', {data['answers'][i]},
                                            '{data['condition_value'][i]}', {image_id}, {data['condition_id'][i]})
                                    """)
            await conn.execute(f"""
                                   update users_information
                                        set communication_conditions = array_append(communication_conditions, {condition_id})
                                    where user_id = {user_id}
                                """)

    @staticmethod
    async def create_user(data, token):
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
                                   insert into users_main (user_id, user_name, email, phone) values(
                                   {id}, '{data['user_name']}', '{data['email']}', '{data['phone']}')
                                   """)
            await conn.execute(f"""
                                   insert into authentication (email, phone, user_name, password, second_authentication, 
                                   user_id, verified, verifying_token) values(
                                   '{data['email']}', '{data['phone']}', '{data['user_name']}', '{data['password']}',
                                   False, {id}, False, '{token}')
                                   """)
            await conn.execute(f"""
                                insert INTO users_information (user_id, country_id, city_id, sex, date_born, age, bio, name, 
                                    surname, relation_ship_id, language_id, wedding, communication_conditions, status_work, 
                                    position, company_id, school_id, bachelor_id, master_id, image_id, achievements_id, 
                                    achievements_desired_id, services_id, services_username,
                                    community_id, community_owner_id) values(
                                    {id}, null, null, null, null, null, null, null, null,
                                    ARRAY []::integer[], null, null, ARRAY []::text[], null, null, null, null, null, 
                                    null, ARRAY []::integer[], ARRAY []::integer[], ARRAY []::integer[], 
                                    ARRAY []::integer[], ARRAY []::varchar[], ARRAY []::integer[], ARRAY []::integer[])
                                """)
            await conn.execute(f"""
                                    insert into user_statistics (user_id, subscribers, likes, comments, recommendations, 
                                        create_achievements, create_courses, create_communities, reach_achievements, 
                                        join_courses, join_communities, posts, completed_courses) values(
                                        {id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                                    """)
            await conn.execute(f"""
                                    insert into user_calendar (user_id, from_date, to_date, free) values(
                                    {id}, null, null, null)
                                    """)

            result = await conn.execute(f"""
                                            insert into subscribes (relationship_id, user_id, users_id, status_id, 
                                                last_update) 
                                            values(
                                            {id}, {id}, ARRAY []::integer[], ARRAY []::integer[], null)
                                            """)

            return result
        else:
            return dict(error='Missing user data parameters')


class UserVerifyAvatar:
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
    async def save_avatar_url(user_id: str, url: str):
        conn = await asyncpg.connect(connection_url)
        if url is not None and user_id is not None:
            image_id = await conn.fetchrow(f"""SELECT MAX(image_id) FROM images""")
            image_id = dict(image_id)['max']
            if image_id is not None:
                image_id = int(image_id) + 1
            else:
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

