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
                             insert into communities (community_id, community_type, community_name, community_bio, user_id, community_owner_id, created_date)
                             values({id}, '{data['community_type']}', '{data['name']}', '{data['bio']}', array_append(users_id, {user_id}), {user_id}, statement_timestamp())
                             """)
        await conn.execute(f"""
                                update users_information 
                                set community_id = array_append(community_id, {id}),
                                    community_owner_id = array_append(community_owner_id, {id})
                                where user_id = {user_id}
                            """)
        #todo: add to users_informaton

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
                                           select u.user_id, u.name, u.surname, c.community_id, c.community_name, c.community_type, c.community_bio, c.community_conditions, c.created_date, c.image_id
                                           from users_information as u
                                           right join (select community_id, community_name, community_type, unnest(user_id) as user_id, community_bio, unnest(community_conditions) as community_conditions, created_date, image_id
                                                        from communities) as c on c.user_id = u.user_id
                                           where c.community_id = {community_id}
                                           """)
        return communities
