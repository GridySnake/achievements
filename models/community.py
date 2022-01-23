import asyncpg
from config.common import BaseConfig

connection_url = BaseConfig.database_url


class CommunityGetInfo:

    @staticmethod
    async def get_user_communities(user_id):
        conn = await asyncpg.connect(connection_url)
        communities = await conn.fetch(f"""
                                          select c.community_id, c.community_name, s.sphere_name, s.subsphere_name
                                          from communities as c
                                          right join (
                                                      select unnest(community_id) as community_id from users_information where user_id={user_id}
                                                      ) as u on u.community_id = c.community_id
                                          left join (
                                                        select c.community_id, array_agg(s.subsphere_name) as subsphere_name, 
                                                        array_agg(s.sphere_name) as sphere_name
                                                        from communities as c
                                                        left join spheres s on s.subsphere_id = any(c.subsphere_id)
                                                        group by c.community_id
                                                    ) s on c.community_id = s.community_id
                                          """)
        return communities

    @staticmethod
    async def get_user_owner_communities(user_id):
        conn = await asyncpg.connect(connection_url)
        communities = await conn.fetch(f"""
                                           select c.community_id, c.community_name, s.sphere_name, s.subsphere_name
                                           from (
                                                 select community_id, community_name, unnest(community_owner_id) as community_owner_id from communities) as c
                                           right join (
                                                       select unnest(community_owner_id) as community_owner_id from users_information where user_id = {user_id}
                                                       ) as u on u.community_owner_id = c.community_owner_id
                                           left join (
                                                        select c.community_id, array_agg(s.subsphere_name) as subsphere_name, 
                                                        array_agg(s.sphere_name) as sphere_name
                                                        from communities as c
                                                        left join spheres s on s.subsphere_id = any(c.subsphere_id)
                                                        group by c.community_id
                                                    ) s on c.community_id = s.community_id
                                           """)
        return communities

    @staticmethod
    async def get_community_info(community_id):
        conn = await asyncpg.connect(connection_url)
        community = await conn.fetchrow(f"""
                                           select u.user_id, u.name, u.surname, c.community_id, c.community_name, c.community_type, c.community_bio, c.condition_id, c.created_date, i.href, c.community_owner_id
                                           from users_information as u
                                           right join (select community_id, community_name, community_type, unnest(user_id) as user_id, community_bio, unnest(condition_id) as condition_id, created_date, image_id, unnest(community_owner_id) as community_owner_id
                                                        from communities) as c on c.user_id = u.user_id
                                           left join images as i on i.image_id = c.image_id[array_upper(c.image_id, 1)] and i.image_type = 'community'
                                           where c.community_id = {community_id}
                                           """)
        return community

    @staticmethod
    async def get_community_participants(community_id):
        conn = await asyncpg.connect(connection_url)
        community = await conn.fetch(f"""
                                            select u.user_id, u.name, u.surname
                                            from users_information as u
                                            right join (select community_id, unnest(user_id) as user_id
                                                         from communities) as c on c.user_id = u.user_id
                                            where c.community_id = {community_id}
                                        """)
        return community

    @staticmethod
    async def get_generate_conditions():
        conn = await asyncpg.connect(connection_url)
        conditions = await conn.fetch(f"""
                                    select condition_id, condition_name, condition_description, community_type
                                    from community_conditions_generate
                                """)
        return conditions

    @staticmethod
    async def user_requests(user_id: str):
        conn = await asyncpg.connect(connection_url)
        conditions = await conn.fetch(f"""
                                        select community_id, community_name
                                        from communities
                                        where {user_id} = any(requests) 
                                        and request_statuses[array_position(requests, {user_id})] = 1
                                    """)
        return conditions


class CommunityAvatarAction:
    @staticmethod
    async def save_community_avatar_url(community_id, url):
        conn = await asyncpg.connect(connection_url)
        image_id = await conn.fetchrow(f"""select max(image_id) from images""")
        image_id = dict(image_id)['max']
        if image_id is not None:
            image_id = int(image_id) + 1
        else:
            image_id = 0
        await conn.execute(f"""
                               insert into images (image_id, href, image_type, create_date) values(
                               {image_id}, '{url}', 'community', statement_timestamp())
                               """)
        await conn.execute(f"""
                               update communities
                               set image_id = array_append(image_id, {image_id})
                               where community_id = {community_id}
                               """)

    @staticmethod
    async def leave_join(community_id, method, user_id):
        conn = await asyncpg.connect(connection_url)
        if method == 'join':
            await conn.execute(f"""
                                   update communities
                                   set user_id = array_append(user_id, {user_id})
                                   where community_id = {community_id}
                                   """)
            await conn.execute(f"""
                                   update users_information
                                   set community_id = array_append(community_id, {community_id})
                                   where user_id = {user_id}
                                   """)
        else:
            await conn.execute(f"""
                                   update communities
                                   set user_id = user_id[:(select array_position(user_id, {user_id})
                                                   FROM communities
                                                   WHERE community_id = {community_id})-1] ||
                                                   user_id[(select array_position(user_id, {user_id})
                                                   FROM communities
                                                   WHERE community_id = {community_id})+1:]
                                   WHERE community_id = {community_id}
                                   """)
            await conn.execute(f"""
                                   update users_information
                                   set community_id = community_id[:(select array_position(community_id, {community_id})
                                                   FROM users_information
                                                   WHERE user_id = {user_id})-1] ||
                                                   community_id[(select array_position(community_id, {community_id})
                                                   FROM users_information
                                                   WHERE user_id = {user_id})+1:]
                                   WHERE user_id = {user_id}
                                   """)

    @staticmethod
    async def add_member(community_id: str, users: list, status: list):
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
                               update communities
                                    set requests = array_cat(requests, array{users}),
                                        request_statuses = array_cat(requests, {status})
                                    where community_id = {community_id}
                            """)

    @staticmethod
    async def remove_member(community_id: str, users: list):
        conn = await asyncpg.connect(connection_url)
        for i in users:
            await conn.execute(f"""
                                   update communities
                                        set user_id = array_remove(user_id, {i})
                                        where community_id = {community_id}
                                """)

    @staticmethod
    async def accept_decline_request(user_id: str, action: int, community_id: str):
        conn = await asyncpg.connect(connection_url)
        if action == 0:
            await conn.execute(f"""
                                    update communities
                                        set requests = array_cat(requests[:array_position(requests, {user_id})-1],
                                                                requests[array_position(requests, {user_id})+1:]),
                                            request_statuses = array_cat(request_statuses[:array_position(requests, {user_id})-1],
                                                                request_statuses[array_position(requests, {user_id})+1:])
                                        where community_id = {community_id}
                                """)
        else:
            await conn.execute(f"""
                                   update communities
                                       set user_id = array_append(user_id, {user_id}),
                                            requests = array_cat(requests[:array_position(requests, {user_id})-1],
                                                                requests[array_position(requests, {user_id})+1:]),
                                            request_statuses = array_cat(request_statuses[:array_position(requests, {user_id})-1],
                                                                request_statuses[array_position(requests, {user_id})+1:])
                                       where community_id = {community_id}
                                """)
            await conn.execute(f"""
                                   update users_information
                                        set community_id = array_append(community_id, {community_id})
                                   where user_id = {user_id}
                                """)


class CommunityCreate:
    @staticmethod
    async def create_community(user_id, data):
        conn = await asyncpg.connect(connection_url)
        id = await conn.fetchrow(f"""
                                  select max(community_id)
                                  from communities
                                """)
        id = dict(id)['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        chat_id = await conn.fetchrow("""select max(chat_id) from chats""")
        chat_id = dict(chat_id)['max']
        if chat_id is not None:
            chat_id += 1
        else:
            chat_id = 0
        await conn.execute(f"""
                               insert into communities (community_id, community_type, community_name, community_bio, user_id, community_owner_id, created_date, image_id, condition_id, condition_value)
                               values({id}, '{data['community_type']}', '{data['name']}', '{data['bio']}', array({user_id}), array({user_id}), statement_timestamp(), ARRAY []::integer[], ARRAY []::integer[], ARRAY []::text[])
                           """)
        await conn.execute(f"""
                                update users_information 
                                set community_id = array_append(community_id, {id}),
                                    community_owner_id = array_append(community_owner_id, {id})
                                where user_id = {user_id}
                            """)
        await conn.execute(f"""
                                insert into chats (chat_id, chat_type, participants, owner_id) values(
                                {chat_id}, 2, array[{user_id}], {id})\
                            """)
