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
        new, course_owner_type, name, surname, community_name
        """
        conn = await asyncpg.connect(connection_url)
        course = await conn.fetchrow(f"""
                                        select c.course_id, c.course_name, c.description, c.course_owner_id, c.sphere,
                                            c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
                                            ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined
                                        from (select * from courses where course_id = {course_id}) as c
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
        new, course_owner_type, name, surname, community_name
        """
        conn = await asyncpg.connect(connection_url)
        courses = await conn.fetch(f"""
                                       select c.course_id, c.course_name, c.description, c.course_owner_id, c.sphere,
                                           c.online, c.free, c.country_id, c.city_id, c.new, c.course_owner_type,
                                           ui.name, ui.surname, com.community_name, array_length(c.users, 1) as joined
                                       from (select * from courses where {user_id} = any(users)) as c
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
