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
        await conn.fetch(f"""
                             insert into communities (community_id, community_type, community_name, community_bio, community_owner_id, created_date)
                             values({id}, '{data['community_type']}', '{data['name']}', '{data['bio']}', '{user_id}', statement_timestamp())
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
                                                          select unnest(community_owner_id) as community_id from users_information where user_id={user_id}
                                                          ) as u on u.community_owner_id = c.community_owner_id

                                              """)
        return communities
