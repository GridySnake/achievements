import hashlib


class UserGetInfo:
    @staticmethod
    async def get_user_by_email_phone(email: str, type: str, conn):
        user = await conn.fetchrow(f"""
        SELECT user_id::varchar, user_name, password
        FROM authentication
        WHERE {type} = '{email}' and verified = True
        """)
        user1 = await conn.fetchrow(f"""
                SELECT user_id
                FROM authentication
                WHERE {type} = '{email}' and verified = False
                """)
        if user:
            user = dict(user)
            return user
        elif user1:
            return 'verify'
        else:
            return dict(error='User with {} {} not found'.format(type, email))

    @staticmethod
    async def get_user_by_id(user_id: str, conn):
        user = await conn.fetchrow(f"""
                                        select name, surname, bio, birthday::varchar, array_agg(i.href) as href
                                        from users_information as ui
                                        left join (select image_id, image_type, href from images order by create_date 
                                            desc) as i on i.image_id = any(ui.image_id)
                                            and image_type='user'
                                        where user_id = {user_id}
                                        group by user_id
                                    """)
        if user:
            user = dict(user)
            return user
        else:
            return None

    @staticmethod
    async def get_user_info_by_value(user_id: str, value: str, conn):
        user = await conn.fetchrow(f"""
                    select {value}
                    from users_information
                    where user_id = {user_id}
                    """)
        return user[value]

    @staticmethod
    async def get_user_info(user_id: str, conn):
        user = await conn.fetchrow(f"""
                            select ui.name, ui.surname, co.country_name_native as country_name, co.country_id, 
                                ci.city_name, ci.city_id, ui.birthday::varchar, ui.bio, um.email, um.phone, um.user_name
                            from users_information as ui
                            left join users_main as um on um.user_id = ui.user_id
                            left join countries as co on co.country_id = ui.country_id
                            left join cities as ci on ci.city_id = ui.city_id
                            left join conditions as con on con.condition_id = any(ui.conditions)
                            where ui.user_id = {user_id}
                            """)
        return dict(user)

    @staticmethod
    async def get_user_info_by_count(user_id: str, value: str, conn):
        count = await conn.fetchrow(f"""
                                      select {value} 
                                      from user_statistics
                                      where user_id = {user_id}
                                    """)
        return count[value]

    @staticmethod
    async def get_avatar_by_user_id(user_id: str, conn):
        avatar = await conn.fetch(f"""
                SELECT us.user_id, images.href
                FROM images
                INNER JOIN users_information as us ON images.image_id = ANY(us.image_id) and images.image_type = 'user'
                WHERE us.user_id = {user_id}
                """)
        if avatar:
            return [dict(i) for i in avatar]
        else:
            return None

    @staticmethod
    async def check_connect(user_id: str, service_id: str, conn):
        count = await conn.fetchrow(f"""select count(services_id)
                                    from users_information
                                    where user_id = {user_id} and {service_id} in (select unnest(services_id) from users_information where user_id={user_id})
        """)
        if count['count'] > 0:
            return True
        else:
            return False

    @staticmethod
    async def get_user_name_by_service(user_id: str, service_id: str, conn):
        username = await conn.fetchrow(f"""select services_username
                                        from users_information
                                        where user_id = {user_id} and {service_id} in (select unnest(services_id) 
                                            from users_information where user_id={user_id})
                                        """)
        return username

    @staticmethod
    async def get_user_conditions(user_active_id: str, user_passive_id: str, conn):
        conditions = await conn.fetch(f"""select c.task, c.condition_value, gc.condition_name, i.href, 
                                            gc.generate_condition_id, case when {user_active_id} = any(c.users_approved)
                                            then true else false end as approved
                                            from users_information as ui
                                            left join conditions as c on
                                                c.condition_id = any(ui.conditions)
                                            left join generate_conditions gc 
                                                on c.generate_condition_id = gc.generate_condition_id
                                            left join images as i on i.image_id = c.image_id
                                            where ui.user_id = {user_passive_id} and 
                                                ({user_active_id} <> any(ui.conditions_approved) or 
                                                ui.conditions_approved = array[]::integer[])
                                    """)
        return [dict(i) for i in conditions]

    @staticmethod
    async def get_community_course_by_type(user_id: str, user_type: str, conn):
        join = {'1': 'c.image_id[array_upper(c.image_id, 1)]', '2': 'c.image_id'}
        table = {'1': 'communities', '2': 'courses'}
        columns = {'1': 'community', '2': 'course'}
        where = {'1': f'any({columns[user_type]}_owner_id)', '2': f'{columns[user_type]}_owner_id'}
        users = await conn.fetch(f"""select c.{columns[user_type]}_id as user_id, 
                                                c.{columns[user_type]}_name as user_name, img.href
                                                from {table[user_type]} as c
                                                left join images as img on img.image_id = {join[user_type]}
                                                where {user_id} = {where[user_type]}
                                        """)
        return [dict(i) for i in users]


class UserCreate:
    @staticmethod
    async def create_user_info(user_id: str, data: dict, conn):
        for i in data.keys():
            if i in ['city', 'country', 'age']:
                await conn.execute(f"""
                                       update users_information
                                       set 
                                           {i} = {data[i]}
                                       where user_id = {user_id}
                                    """)
            else:
                await conn.execute(f"""
                                        update users_information
                                        set 
                                            {i} = '{data[i]}'
                                        where user_id = {user_id}
                                    """)

    @staticmethod
    async def create_user_main(user_id: str, data: dict, conn):
        for i in data.keys():
            await conn.execute(f"""
                                   update users_main
                                   set 
                                       {i} = '{data[i]}'
                                   where user_id = {user_id}
                                """)

    @staticmethod
    async def create_user_info_conditions(user_id: str, data: dict, conn):
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
                                        set conditions = array_append(conditions, {condition_id})
                                    where user_id = {user_id}
                                """)

    @staticmethod
    async def create_user(data, token, conn):
        # TODO: make just phone or email
        email = data['email']
        phone = data['phone']
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
                id = dict(id)['max'] + 1
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
                                    surname, language_id, wedding, conditions, status_work, 
                                    position, company_id, school_id, bachelor_id, master_id, image_id, achievements_id, 
                                    achievements_desired_id, services_id, services_username,
                                    community_id, community_owner_id, age) values(
                                    {id}, null, null, null, null, null, null, null, null,
                                    null, null, ARRAY []::integer[], null, null, null, null, null, 
                                    null, ARRAY []::integer[], ARRAY []::integer[], ARRAY []::integer[], 
                                    ARRAY []::integer[], ARRAY []::varchar[], ARRAY []::integer[], ARRAY []::integer[],
                                    null)
                                """)
            await conn.execute(f"""
                                    insert into user_statistics (user_id, followers, likes, comments, recommendations, 
                                        create_achievements, create_courses, create_communities, achievements, 
                                        join_courses, join_communities, posts, completed_courses, followings) values(
                                        {id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                                    """)
            await conn.execute(f"""
                                    insert into user_calendar (user_id, from_date, to_date, free) values(
                                    {id}, null, null, null)
                                    """)
            await conn.execute(f"""
                                   insert into likes (owner_id, owner_type, users_liked_id, users_liked_type, 
                                       action_datetime) values({id}, 0, array[]::integer[], array[]::integer[],
                                       array[]::timestamptz[])
                                """)
            await conn.execute(f"""
                                   insert into dislikes (owner_id, owner_type, users_disliked_id, users_disliked_type, 
                                       action_datetime) values({id}, 0, array[]::integer[], array[]::integer[],
                                       array[]::timestamptz[])
                                """)
            await conn.execute(f"""
                                   insert into recommendations (owner_id, owner_type, users_recommend_id, 
                                        users_recommend_type, action_datetime) values({id}, 0, array[]::integer[], 
                                        array[]::integer[], array[]::timestamptz[])
                                """)

            result = await conn.execute(f"""
                                            insert into subscribes (relationship_id, user_id, users_id, status_id, 
                                                last_update) 
                                            values({id}, {id}, ARRAY []::integer[], ARRAY []::integer[], null)
                                        """)

            return result
        else:
            return dict(error='Missing user data parameters')


class UserVerifyAvatar:
    @staticmethod
    async def verify_user(href, conn):
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
    async def save_avatar_url(user_id: str, url: str, conn):
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

