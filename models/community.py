import asyncpg
from config.common import BaseConfig

connection_url = BaseConfig.database_url


class Community:
    @staticmethod
    async def create_community(user_id, data):
        conn = await asyncpg.connect(connection_url)
        id = await conn.fetch(f"""
                                  select max(community_id)
                                  from communities
                                """)
        id = dict(id[0])['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        await conn.execute(f"""
                               insert into communities (community_id, community_type, community_name, community_bio, user_id, community_owner_id, created_date, image_id)
                               values({id}, '{data['community_type']}', '{data['name']}', '{data['bio']}', array({user_id}), array({user_id}), statement_timestamp(), ARRAY []::integer[])
                           """)
        await conn.execute(f"""
                                update users_information 
                                set community_id = array_append(community_id, {id}),
                                    community_owner_id = array_append(community_owner_id, {id})
                                where user_id = {user_id}
                            """)

    @staticmethod
    async def get_user_communities(user_id):
        conn = await asyncpg.connect(connection_url)
        communities = await conn.fetch(f"""
                                          select c.community_id, c.community_name
                                          from communities as c
                                          right join (
                                                      select unnest(community_id) as community_id from users_information where user_id={user_id}
                                                      ) as u on u.community_id = c.community_id
                                           
                                          """)
        return communities

    @staticmethod
    async def get_user_owner_communities(user_id):
        conn = await asyncpg.connect(connection_url)
        communities = await conn.fetch(f"""
                                           select c.community_id, c.community_name
                                           from communities as c
                                           right join (
                                                       select unnest(community_owner_id) as community_owner_id from users_information where user_id={user_id}
                                                       ) as u on u.community_owner_id = c.community_owner_id
                                           """)
        return communities

    @staticmethod
    async def get_community_info(community_id):
        conn = await asyncpg.connect(connection_url)
        communities = await conn.fetch(f"""
                                           select u.user_id, u.name, u.surname, c.community_id, c.community_name, c.community_type, c.community_bio, c.community_conditions, c.created_date, i.href, c.community_owner_id
                                           from users_information as u
                                           right join (select community_id, community_name, community_type, unnest(user_id) as user_id, community_bio, unnest(community_conditions) as community_conditions, created_date, unnest(image_id) as image_id, unnest(community_owner_id) as community_owner_id
                                                        from communities) as c on c.user_id = u.user_id
                                           left join images as i on i.image_id = c.image_id and i.image_type = 'community'
                                           where c.community_id = {community_id}
                                           """)
        return communities

    @staticmethod
    async def save_community_avatar_url(community_id, url):
        conn = await asyncpg.connect(connection_url)
        image_id = await conn.fetchrow(f"""select max(image_id) from images""")
        print(image_id)
        image_id = dict(image_id)['max']
        if image_id is not None:
            image_id = int(image_id) + 1
        else:
            image_id = 0
        await conn.execute(f"""
                               insert into images (image_id, href, image_type, create_date) values(
                               {image_id}, '{url}', 'user', statement_timestamp())
                               """)
        await conn.execute(f"""
                               update communities
                               set image_id = array_append(image_id, {image_id})
                               where community_id = {community_id}
                               """)
