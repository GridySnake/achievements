import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


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
    async def get_user_course_suggestions(user_id: str):
        """
        :param user_id: str
        :return: list of asyncpg records: course_id, course_name, description, course_owner_id, sphere, online, free,
        new, course_owner_type, name, surname, community_name
        """
        conn = await asyncpg.connect(connection_url)
        courses = await conn.fetch(f"""
                                        select c.course_id, c.course_name, c.description, c.course_owner_id, c.sphere_id,
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
        return courses

    @staticmethod
    async def get_course_info(course_id: str):
        """
        :param course_id: str
        :return: asyncpg record: course_id, course_name, description, course_owner_id, sphere, online, free,
        new, course_owner_type, name, surname, community_name, language
        """
        conn = await asyncpg.connect(connection_url)
        course = await conn.fetchrow(f"""
                                        select c.course_id, c.course_name, c.description, c.course_owner_id, 
                                            c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
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
    async def get_user_courses(user_id: str):
        """
        :param user_id: str
        :return: asyncpg records: course_id, course_name, description, course_owner_id, sphere, online, free,
        new, course_owner_type, name, surname, community_name, language
        """
        conn = await asyncpg.connect(connection_url)
        courses = await conn.fetch(f"""
                                       select c.course_id, c.course_name, c.description, c.course_owner_id,
                                           c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
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
        return courses

    @staticmethod
    async def get_own_courses(user_id: str):
        """
        :param user_id: str
        :return: asyncpg records: course_id, course_name, description, course_owner_id, sphere, online, free,
        new, course_owner_type, name, surname, community_name, language
        """
        conn = await asyncpg.connect(connection_url)
        courses = await conn.fetch(f"""
                                       select c.course_id, c.course_name, c.description, c.course_owner_id, c.sphere_id,
                                          c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
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
        return courses

    @staticmethod
    async def is_user_in_course(course_id: str, user_id: str):
        """
        :param course_id: str
        :param user_id: str
        :return: bool
        """
        conn = await asyncpg.connect(connection_url)
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
    async def is_owner(course_id: str, user_id: str):
        conn = await asyncpg.connect(connection_url)
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
    async def get_course_participants(course_id: str):
        conn = await asyncpg.connect(connection_url)
        participants = await conn.fetch(f"""
                                               select u.user_id, u.name, u.surname
                                               from (select course_id, unnest(users) as users from courses) as c
                                               left join users_information as u on u.user_id = c.users
                                               where c.course_id = {course_id}
                                            """)
        return participants

    @staticmethod
    async def user_requests(user_id: str):
        conn = await asyncpg.connect(connection_url)
        requests = await conn.fetch(f"""
                                        select c.course_id, c.course_name
                                        from courses as c
                                        where {user_id} = any(requests)
                                         and request_statuses[array_position(requests, {user_id})] = 1
                                    """)
        return requests


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
    async def join_course(course_id: str, user_id: str):
        """
        :param course_id: str
        :param user_id: str
        :return: None
        """
        conn = await asyncpg.connect(connection_url)
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
    async def leave_course(course_id: str, user_id: str):
        """
        :param course_id: str
        :param user_id: str
        :return: None
        """
        conn = await asyncpg.connect(connection_url)
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
    async def add_member(course_id: str, users: list, status: list):
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
                                update courses
                                    set requests = array_cat(requests, array{users}),
                                        request_statuses = array_cat(request_statuses, array{status})
                                where course_id = {course_id}
                            """)

    @staticmethod
    async def accept_decline_request(user_id: str, action: int, course_id: str):
        conn = await asyncpg.connect(connection_url)
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
    async def create_course(user_id: str, data: dict, no_image: bool):
        """
        :param user_id: str
        :param data: dict: course_name, description, language, level, online, free, image_id
        :param no_image: bool
        :return: None
        """
        conn = await asyncpg.connect(connection_url)
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


class CourseContentModel:
    @staticmethod
    async def count_course_content(course_id: str):
        conn = await asyncpg.connect(connection_url)
        content = await conn.fetchrow(f"""
                                        select count(content_id)
                                        from courses_content
                                        where course_id = {course_id}
                                    """)
        return content['count']

    @staticmethod
    async def course_content_page(course_id: str, page: str):
        conn = await asyncpg.connect(connection_url)
        content = await conn.fetchrow(f"""
                                       select content_type, content_name, content_description, content_path
                                       from courses_content
                                       where course_id = {course_id} and content_page = {page}
                                    """)
        return content

    @staticmethod
    async def course_content_navigation(course_id: str):
        conn = await asyncpg.connect(connection_url)
        content = await conn.fetch(f"""
                                        select content_name, is_title, is_subtitle, content_page
                                        from courses_content
                                        where course_id = {course_id}
                                        order by content_page
                                    """)
        return content

    @staticmethod
    async def course_create_content(course_id: str, content: dict):
        conn = await asyncpg.connect(connection_url)
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

