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
                                        select c.course_id, c.course_name, c.description, c.course_owner_id, c.sphere,
                                            c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
                                            ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined
                                        from courses as c
                                        left join users_information as ui on ui.user_id = c.course_owner_id
                                            and c.course_owner_type = 0
                                        left join communities as com on com.community_id = c.course_owner_id
                                            and c.course_owner_type = 1 and {user_id} <> any(com.community_owner_id)
                                        where {user_id} <> all(c.users) and c.course_owner_id <> {user_id}
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
                                        select c.course_id, c.course_name, c.description, c.course_owner_id, c.sphere,
                                            c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
                                            ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined,
                                            l.language_native
                                        from (select * from courses where course_id = {course_id}) as c
                                        left join languages as l on l.language_id = c.language
                                        left join users_information as ui on ui.user_id = c.course_owner_id
                                            and c.course_owner_type = 0
                                        left join communities as com on com.community_id = c.course_owner_id
                                            and c.course_owner_type = 1
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
                                       select c.course_id, c.course_name, c.description, c.course_owner_id, c.sphere,
                                           c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
                                           ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined,
                                           l.language_native
                                       from (select * from courses where {user_id} = any(users)) as c
                                       left join languages as l on l.language_id = c.language
                                       left join users_information as ui on ui.user_id = c.course_owner_id
                                           and c.course_owner_type = 0
                                       left join communities as com on com.community_id = c.course_owner_id
                                           and c.course_owner_type = 1
            """)
        return courses

    @staticmethod
    async def get_own_courses(user_id: str):
        """
        :param user_id: str
        :return: asyncpg records: course_id, course_name, description, course_owner_id, sphere, online, free,
        new, course_owner_type, name, surname, community_name, language
        """
        # todo: сделать разбивку по юзеру и его коммьюнити
        conn = await asyncpg.connect(connection_url)
        courses = await conn.fetch(f"""
                                       select c.course_id, c.course_name, c.description, c.course_owner_id, c.sphere,
                                          c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
                                          ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined,
                                          l.language_native
                                       from (select * from courses where {user_id} = course_owner_id) as c
                                       left join languages as l on l.language_id = c.language
                                       left join users_information as ui on ui.user_id = c.course_owner_id
                                          and c.course_owner_type = 0
                                       left join communities as com on com.community_id = c.course_owner_id
                                          and c.course_owner_type = 1
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
                                    set courses = array_append(courses, {course_id})
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
                                   set courses = courses[:(select array_position(courses, {course_id}) 
                                                    from users_information
                                                    where user_id = {user_id})-1] || 
                                                    courses[(select array_position(courses, {course_id}) 
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
        await conn.execute(f"""
                                insert into courses (course_id, course_owner_id, users, course_owner_type, 
                                description, level, online, create_date, free, new, sphere, 
                                language, course_name, image_id)
                                values ({course_id}, {user_id}, ARRAY []::integer[], {data['type']}, '{data['description']}',
                                {data['level']}, {data['online']}, statement_timestamp(), {data['free']}, true,
                                '{data['sphere']}', {data['language']}, '{data['course_name']}', {image_id})
                            """)
