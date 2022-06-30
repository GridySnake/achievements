class CoursesGetInfo:
    """
        Class for getting information for subscribes
        ...
        Attributes
        ----------
        None

        Methods
        -------
        get_user_course_suggestions(user_id: str)
            Give courses witch have no connection to user
        get_course_info(course_id: str)
            Give information about course
    """
    @staticmethod
    async def get_user_course_suggestions(user_id: str, conn):
        """
        :param conn:
        :param user_id: str
        :return: list of asyncpg records: course_id, course_name, description, course_owner_id, sphere, online, free,
        new, course_owner_type, name, surname, community_name
        """
        courses = await conn.fetch(f"""
                                        select c.course_id:: varchar, c.course_name, c.description, c.course_owner_id,
                                            c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
                                            ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined,
                                            s.sphere_name, s.subsphere_name
                                            from (select * from courses where {user_id} <> all(users) 
                                            and ({user_id} <> any(requests) or requests = array[]::integer[])) as c
                                        left join users_information as ui on ui.user_id = c.course_owner_id
                                            and c.course_owner_type = 0  and course_owner_id <> {user_id}
                                        left join communities as com on com.community_id = c.course_owner_id
                                            and c.course_owner_type = 1 and {user_id} <> any(com.community_owner_id)
                                        left join (
                                                    select c.course_id, array_agg(s.subsphere_name) as subsphere_name, 
                                                           array_agg(s.sphere_name) as sphere_name
                                                    from courses as c
                                                    left join spheres s on s.subsphere_id = any(c.subsphere_id)
                                                    group by c.course_id
                                                ) as s on c.course_id = s.course_id
                                        order by new desc
        """)
        return [dict(i) for i in courses]

    @staticmethod
    async def get_course_info_by_value(course_id: str, value: str, conn):
        course = await conn.fetchrow(f"""
                                      select {value} 
                                      from course_statistics
                                      where course_id = {course_id}
                                    """)
        return course[value]

    @staticmethod
    async def get_course_info(course_id: str, conn):
        """
        :param conn:
        :param course_id: str
        :return: asyncpg record: course_id, course_name, description, course_owner_id, sphere, online, free,
        new, course_owner_type, name, surname, community_name, language
        """
        course = await conn.fetchrow(f"""
                                        select c.course_id:: varchar, c.course_name, c.description, c.course_owner_id, 
                                            c.online, c.free, c.new, c.course_owner_type,
                                            ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined,
                                            l.language_native, c.subsphere_id
                                        from (select * from courses where course_id = {course_id}) as c
                                        left join languages as l on l.language_id = c.language
                                        left join users_information as ui on ui.user_id = c.course_owner_id
                                            and c.course_owner_type = 0
                                        left join communities as com on com.community_id = c.course_owner_id
                                            and c.course_owner_type = 1
                                        left join (
                                                    select c.course_id, array_agg(s.subsphere_name) as subsphere_name, 
                                                           array_agg(s.sphere_name) as sphere_name
                                                    from courses as c
                                                    left join spheres s on s.subsphere_id = any(c.subsphere_id)
                                                    group by c.course_id
                                                ) as s on c.course_id = s.course_id
        """)
        return course

    @staticmethod
    async def get_user_courses(user_id: str, conn):
        """
        :param conn:
        :param user_id: str
        :return: asyncpg records: course_id, course_name, description, course_owner_id, sphere, online, free,
        new, course_owner_type, name, surname, community_name, language
        """
        courses = await conn.fetch(f"""
                                       select c.course_id:: varchar, c.course_name, c.description, c.course_owner_id:: varchar,
                                           c.online, c.free, c.new, c.course_owner_type,
                                           ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined,
                                           l.language_native, s.sphere_name, s.subsphere_name
                                       from (select * from courses where {user_id} = any(users)) as c
                                       left join languages as l on l.language_id = c.language
                                       left join users_information as ui on ui.user_id = c.course_owner_id
                                           and c.course_owner_type = 0  and course_owner_id <> {user_id}
                                       left join communities as com on com.community_id = c.course_owner_id
                                           and c.course_owner_type = 1  and {user_id} <> any(com.community_owner_id)
                                       left join (
                                                    select c.course_id, array_agg(s.subsphere_name) as subsphere_name, 
                                                           array_agg(s.sphere_name) as sphere_name
                                                    from courses as c
                                                    left join spheres s on s.subsphere_id = any(c.subsphere_id)
                                                    group by c.course_id
                                                ) as s on c.course_id = s.course_id
            """)
        return [dict(i) for i in courses]

    @staticmethod
    async def get_own_courses(user_id: str, conn):
        """
        :param conn:
        :param user_id: str
        :return: asyncpg records: course_id, course_name, description, course_owner_id, sphere, online, free,
        new, course_owner_type, name, surname, community_name, language
        """
        courses = await conn.fetch(f"""
                                       select c.course_id:: varchar, c.course_name, c.description, c.course_owner_id:: varchar, c.sphere_id,
                                          c.online, c.free, c.new, c.course_owner_type,
                                          ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined,
                                          l.language_native, s.sphere_name, s.subsphere_name
                                       from (select * from courses where {user_id} = course_owner_id) as c
                                       left join languages as l on l.language_id = c.language
                                       left join users_information as ui on ui.user_id = c.course_owner_id
                                          and c.course_owner_type = 0
                                       left join communities as com on com.community_id = c.course_owner_id
                                          and c.course_owner_type = 1
                                        left join (
                                            select c.course_id, array_agg(s.subsphere_name) as subsphere_name, 
                                            array_agg(s.sphere_name) as sphere_name
                                            from courses as c
                                            left join spheres s on s.subsphere_id = any(c.subsphere_id)
                                            group by c.course_id
                                           ) s on c.course_id = s.course_id
                                    """)
        return [dict(i) for i in courses]

    @staticmethod
    async def is_user_in_course(course_id: str, user_id: str, conn):
        """
        :param conn:
        :param course_id: str
        :param user_id: str
        :return: bool
        """
        result = await conn.fetchrow(f"""
                                        select
                                        case
                                            when count(c.course_id) > 0 then true
                                            else false
                                        end as result
                                        from (select * from courses where course_id = {course_id} 
                                            and {user_id} = any(users)) as c
                                        """)
        return result['result']

    @staticmethod
    async def is_owner(course_id: str, user_id: str, conn):
        owner = await conn.fetchrow(f"""
                                        select 
                                            case when u.user_id is not null then true
                                                when u1.user_id is not null then true
                                                else false
                                            end
                                                as is_owner
                                        from (select course_owner_id, course_owner_type from courses where course_id = {course_id}) as c
                                        left join users_information as u on u.user_id = c.course_owner_id
                                          and c.course_owner_type = 0 and u.user_id = {user_id}
                                        left join (select community_id, unnest(community_owner_id) as owner_id from communities) as com
                                            on com.community_id = c.course_owner_id
                                          and c.course_owner_type = 1
                                        left join users_information as u1 on u1.user_id = com.owner_id
                                            and u1.user_id = {user_id}
                                    """)
        return owner['is_owner']

    @staticmethod
    async def get_course_participants(course_id: str, conn):
        participants = await conn.fetch(f"""
                                               select u.user_id:: varchar, u.name, u.surname
                                               from (select course_id, unnest(users) as users from courses) as c
                                               left join users_information as u on u.user_id = c.users
                                               where c.course_id = {course_id}
                                            """)
        return participants

    @staticmethod
    async def user_requests(user_id: str, conn):
        course_requests = await conn.fetch(f"""
                                        select c.course_id:: varchar, c.course_name
                                        from courses as c
                                        where {user_id} = any(requests)
                                         and request_statuses[array_position(requests, {user_id})] = 1
                                    """)
        return [dict(i) for i in course_requests]

    @staticmethod
    async def get_course_conditions(user_id: str, course_id: str, conn):
        conditions = await conn.fetch(f"""select c.task, c.condition_value, gc.condition_name, i.href, 
                                            gc.generate_condition_id, case when {user_id} = any(c.users_approved)
                                            then true else false end as approved, case when {user_id} = 
                                                cl.user_id then true else false end as cl_send, case when {user_id} = 
                                                int.user_id then true else false end as int_send
                                            from courses as cor
                                            left join conditions as c on
                                                c.condition_id = any(cor.conditions)
                                            left join generate_conditions gc 
                                                on c.generate_condition_id = gc.generate_condition_id
                                            left join images as i on i.image_id = c.image_id
                                            left join cover_letters as cl on cl.cover_letter_id = any(cor.cover_letters)
                                            left join interviews as int on int.interview_id = any(cor.interviews)
                                            where cor.course_id = {course_id} and 
                                                ({user_id} <> any(cor.conditions_approved) or 
                                                cor.conditions_approved = array[]::integer[])
                                    """)
        return conditions

    @staticmethod
    async def get_assistant_courses(user_id, conn):
        assistant_courses = await conn.fetch(f"""
                                                select c.course_id:: varchar, c.course_name, c.description,
                                          c.online, c.free, c.new, c.course_owner_type,
                                          ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined,
                                          l.language_native, s.sphere_name, s.subsphere_name
                                       from (select * from courses where {user_id} = any(assistants)) as c
                                       left join languages as l on l.language_id = c.language
                                       left join users_information as ui on ui.user_id = c.course_owner_id
                                          and c.course_owner_type = 0
                                       left join communities as com on com.community_id = c.course_owner_id
                                          and c.course_owner_type = 1
                                        left join (
                                            select c.course_id, array_agg(s.subsphere_name) as subsphere_name, 
                                            array_agg(s.sphere_name) as sphere_name
                                            from courses as c
                                            left join spheres s on s.subsphere_id = any(c.subsphere_id)
                                            group by c.course_id
                                           ) s on c.course_id = s.course_id
                                            """)
        return [dict(i) for i in assistant_courses]


class CoursesAction:
    """
    Class for make actions in courses (join, leave)
    ...
    Attributes
    ----------
    None

    Methods
    -------
    join_course(course_id: str, user_id: str)
        Join user to course
    leave_course(course_id: str, user_id: str)
        Drop user from course
    """
    @staticmethod
    async def join_course(course_id: str, user_id: str, conn):
        """
        :param conn:
        :param course_id: str
        :param user_id: str
        :return: None
        """
        await conn.execute(f"""
                                update users_information
                                    set course_id = array_append(course_id, {course_id})
                                where user_id = {user_id}
                            """)
        await conn.execute(f"""
                               update courses
                                   set users = array_append(users, {user_id})
                               where course_id = {course_id}
                            """)
        event_id = await conn.fetchrow("""select max(event_id) from courses_events""")
        event_id = dict(event_id)['max']
        if event_id is None:
            event_id = 0
        else:
            event_id += 1
        await conn.execute(f"""
                               insert into courses_events (event_id, course_id, user_id, status) 
                               values({event_id}, {course_id}, {user_id}, 1)
                             """)

    @staticmethod
    async def leave_course(course_id: str, user_id: str, conn):
        """
        :param course_id: str
        :param user_id: str
        :return: None
        """
        await conn.execute(f"""
                               update users_information
                                   set course_id = course_id[:(select array_position(course_id, {course_id}) 
                                                    from users_information
                                                    where user_id = {user_id})-1] || 
                                                    course_id[(select array_position(course_id, {course_id}) 
                                                    from users_information
                                                    where user_id = {user_id})+1:]
                               where user_id = {user_id}
                            """)
        await conn.execute(f"""
                               update courses
                                   set users = users[:(select array_position(users, {user_id}) 
                                                    from courses
                                                    where course_id = {course_id})-1] || 
                                                    users[(select array_position(users, {user_id}) 
                                                    from courses
                                                    where course_id = {course_id})+1:]
                               where course_id = {course_id}
                            """)
        event_id = await conn.fetchrow("""select max(event_id) from courses_events""")
        event_id = dict(event_id)['max']
        if event_id is None:
            event_id = 0
        else:
            event_id += 1
        await conn.execute(f"""
                                insert into courses_events (event_id, course_id, user_id, status) 
                                values({event_id}, {course_id}, {user_id}, 0)
                            """)
        await conn.execute(f"""
                               update users_information
                                    set course_id = array_remove(course_id, {course_id})
                               where user_id = {user_id}
                            """)

    @staticmethod
    async def add_member(course_id: str, users: list, status: list, conn):
        await conn.execute(f"""
                                update courses
                                    set requests = array_cat(requests, array[{users}]),
                                        request_statuses = array_cat(request_statuses, array[{status}])
                                where course_id = {course_id}
                            """)

    @staticmethod
    async def accept_decline_request(user_id: str, action: int, course_id: str, conn):
        if action == 0:
            await conn.execute(f"""
                                    update courses
                                        set requests = array_cat(requests[:array_position(requests, {user_id})-1],
                                                                requests[array_position(requests, {user_id})+1:]),
                                            request_statuses = array_cat(request_statuses[:array_position(requests, {user_id})-1],
                                                                request_statuses[array_position(requests, {user_id})+1:])
                                        where course_id = {course_id}
                                """)
        else:
            await conn.execute(f"""
                                   update courses
                                       set users = array_append(users, {user_id}),
                                            requests = array_cat(requests[:array_position(requests, {user_id})-1],
                                                                requests[array_position(requests, {user_id})+1:]),
                                            request_statuses = array_cat(request_statuses[:array_position(requests, {user_id})-1],
                                                                request_statuses[array_position(requests, {user_id})+1:])
                                       where course_id = {course_id}
                                """)
            await conn.execute(f"""
                                   update users_information
                                        set course_id = array_append(course_id, {course_id})
                                   where user_id = {user_id}
                                """)


class CourseCreate:
    """
    Class for creating course and course's content
    ...
    Attributes
    ----------
    None

    Methods
    -------
    create_course(user_id: str, data: dict)
        Creating course

    """

    @staticmethod
    async def create_course(user_id: str, data: dict, no_image: bool, conn):
        """
        :param user_id: str
        :param data: dict: course_name, description, language, level, online, free, image_id
        :param no_image: bool
        :return: None
        """
        if no_image:
            image_id = 'null'
        else:
            image_id = await conn.fetchrow("""select max(image_id) from images""")
            image_id = dict(image_id)['max']
            if image_id is None:
                image_id = 0
            else:
                image_id += 1
            await conn.execute(f"""
                                   insert into images (image_id, image_type, create_date, href)
                                   values ({image_id}, 'course', statement_timestamp(), '{data['avatar']}')
                                """)
        course_id = await conn.fetchrow("""select max(course_id) from courses""")
        course_id = dict(course_id)['max']
        if course_id is None:
            course_id = 0
        else:
            course_id += 1
        chat_id = await conn.fetchrow("""select max(chat_id) from chats""")
        chat_id = dict(chat_id)['max']
        if chat_id is not None:
            chat_id += 1
        else:
            chat_id = 0
        await conn.execute(f"""
                                insert into courses (course_id, course_owner_id, users, course_owner_type, 
                                description, level, online, create_date, free, new, 
                                language, course_name, image_id, sphere_id, subsphere_id)
                                values ({course_id}, {user_id}, ARRAY []::integer[], {data['type']}, '{data['description']}',
                                {data['level']}, {data['online']}, statement_timestamp(), {data['free']}, true,
                                {data['language']}, '{data['course_name']}', {image_id}, array[{data['sphere']}],
                                array[{data['select_subsphere']}])
                            """)
        await conn.execute(f"""
                               insert into chats (chat_id, chat_type, participants, owner_id) values(
                               {chat_id}, 3, array[{user_id}], {course_id})
                            """)
        await conn.execute(f"""
                               update users_information
                                    set course_id = array_append(course_id, {course_id})
                               where user_id = {user_id}
                            """)
        await conn.execute(f"""
                               insert into course_statistics (course_id, participants, rating, likes, 
                                    participants_complete_course, comments, create_achievements, recommendation, 
                                    reach_achievements, steps_course, participants_in_progress_course) values(
                                    {course_id}, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                            """)
        await conn.execute(f"""
                                insert into likes (owner_id, owner_type, users_liked_id, users_liked_type, 
                                    action_datetime) values({course_id}, 2, array[]::integer[], array[]::integer[],
                                    array[]::timestamptz[])
                            """)
        await conn.execute(f"""
                               insert into dislikes (owner_id, owner_type, users_disliked_id, users_disliked_type, 
                                   action_datetime) values({course_id}, 2, array[]::integer[], array[]::integer[],
                                   array[]::timestamptz[])
                            """)
        await conn.execute(f"""
                               insert into recommendations (owner_id, owner_type, users_recommend_id, 
                                    users_recommend_type, action_datetime) values({course_id}, 2, array[]::integer[], 
                                    array[]::integer[], array[]::timestamptz[])
                            """)
        return course_id

    @staticmethod
    async def create_course_info_conditions(course_id: str, data: dict, conn):
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
                                   update courses
                                        set conditions = array_append(conditions, {condition_id})
                                    where course_id = {course_id}
                                """)


class CourseContentModel:
    @staticmethod
    async def count_course_content(course_id: str, conn):
        content = await conn.fetchrow(f"""
                                        select count(content_id)
                                        from courses_content
                                        where course_id = {course_id}
                                    """)
        return content['count']

    @staticmethod
    async def course_content_page(course_id: str, page: str, conn):
        content = await conn.fetchrow(f"""
                                       select content_type, content_name, content_description, content_path
                                       from courses_content
                                       where course_id = {course_id} and content_page = {page}
                                    """)
        return content

    @staticmethod
    async def course_content_navigation(course_id: str, conn):
        content = await conn.fetch(f"""
                                        select content_name, is_title, is_subtitle, content_page
                                        from courses_content
                                        where course_id = {course_id}
                                        order by content_page
                                    """)
        return content

    @staticmethod
    async def course_create_content(course_id: str, content: dict, conn):
        content_id = await conn.fetchrow("""select max(content_id) from courses_content""")
        content_type_dict = {'document': 0, 'photo': 1, 'video': 2, 'PDF': 3, 'test': 4}
        if content_id['max'] is None:
            content_id = -1
        else:
            content_id = content_id['max']
        for i in range(len(content['name'])):
            content_id += 1
            await conn.execute(f"""
                                   insert into courses_content (content_id, content_name, content_description, 
                                       content_type, content_path, is_title, is_subtitle, course_id, content_page) 
                                       values({content_id}, '{content['name'][i]}', '{content['description'][i]}', 
                                       '{content_type_dict[content['type'][i]]}', '{content['path'][i]}', 
                                       {content['chapter'][i]}, {content['subchapter'][i]}, {course_id}, 
                                       {content['page'][i]})
                                """)

