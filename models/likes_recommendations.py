import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class LikesRecommendationsGetInfo:

    @staticmethod
    async def is_like_recommend(user_id: str, user_type: int, owner_id: str, owner_type: int):
        conn = await asyncpg.connect(connection_url)
        like_rec = await conn.fetchrow(f"""select case when l.owner_id = {owner_id} then true else false end as likes, 
                                                  case when r.owner_id = {owner_id} then true else false end 
                                                  as recommend, case when d.owner_id = {owner_id} then true else false 
                                                  end as dislikes
                                             from users_information as ui
                                             left join (select owner_id from likes where owner_type = {owner_type} 
                                                and {user_id} = any(users_liked_id)
                                                and users_liked_type[array_position(users_liked_type, {user_id})]
                                                = {user_type}) as l on l.owner_id = ui.user_id
                                             left join (select owner_id from recommendations 
                                                where owner_type = {owner_type} and {user_id} = any(users_recommend_id)
                                                and users_recommend_type[array_position(users_recommend_id, {user_id})]
                                                = {user_type}) as r on ui.user_id = r.owner_id
                                             left join (select owner_id from dislikes 
                                                where owner_type = {owner_type} and {user_id} = any(users_disliked_id)
                                                and users_disliked_type[array_position(users_disliked_id, {user_id})]
                                                = {user_type}) as d on ui.user_id = d.owner_id
                                             where ui.user_id = {owner_id}
                                        """)
        return like_rec['likes'], like_rec['recommend'], like_rec['dislikes']

    @staticmethod
    async def get_statistics(owner_id: str, owner_type: str):
        conn = await asyncpg.connect(connection_url)
        statistics = await conn.fetchrow(f"""
                                             select *
                                             from {owner_type}_statistics
                                             where {owner_type}_id = {owner_id}
                                          """)
        return dict(statistics)


class LikesRecommendationsAction:

    @staticmethod
    async def like_recommend(user_id: str, user_type: int, owner_id: str, owner_type: list, like_recommendations: list):
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""update {like_recommendations[0]}
                               set users_{like_recommendations[1]}_id = 
                                        array_append(users_{like_recommendations[1]}_id, {user_id}),
                                    users_{like_recommendations[1]}_type = 
                                        array_append(users_{like_recommendations[1]}_type, {user_type}),
                                    action_datetime = array_append(action_datetime, statement_timestamp())
                                where owner_id = {owner_id} and owner_type = {owner_type[2]}
                            """)
        await conn.execute(f"""update {owner_type[1].replace('id', 'statistics')}
                                    set {like_recommendations[0]} = {like_recommendations[0]} + 1
                                    where {owner_type[1]} = {owner_id}
                            """)

    @staticmethod
    async def unlike_unrecommend(user_id: str, user_type: str, owner_id: str, owner_type: list,
                                 like_recommendations: list):
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
                                update {like_recommendations[0]}
                                    set users_{like_recommendations[1]}_id = 
                                        users_{like_recommendations[1]}_id[:(select 
                                            array_position(f.users_{like_recommendations[1]}_id, {user_id})
                                            from {like_recommendations[0]} as f
                                            where f.owner_id = {owner_id} and f.owner_type={owner_type[2]})-1] ||
                                            users_{like_recommendations[1]}_id[(select 
                                            array_position(f.users_{like_recommendations[1]}_id, {user_id})
                                            from {like_recommendations[0]} as f
                                            where f.owner_id = {owner_id} and f.owner_type={owner_type[2]})+1:],
                                        users_{like_recommendations[1]}_type = 
                                            users_{like_recommendations[1]}_type[:(select 
                                            array_position(f.users_{like_recommendations[1]}_id, {user_id})
                                            from {like_recommendations[0]} as f
                                            where f.owner_id = {owner_id} and f.owner_type={owner_type[2]})-1] ||
                                            users_{like_recommendations[1]}_type[(select 
                                            array_position(f.users_{like_recommendations[1]}_id, {user_id})
                                            from {like_recommendations[0]} as f
                                            where f.owner_id = {owner_id} and f.owner_type={owner_type[2]})+1:],
                                        action_datetime = 
                                            action_datetime[:(select 
                                            array_position(f.users_{like_recommendations[1]}_id, {user_id})
                                            from {like_recommendations[0]} as f
                                            where f.owner_id = {owner_id} and f.owner_type={owner_type[2]})-1] ||
                                            action_datetime[(select 
                                            array_position(f.users_{like_recommendations[1]}_id, {user_id})
                                            from {like_recommendations[0]} as f
                                            where f.owner_id = {owner_id} and f.owner_type={owner_type[2]})+1:]
                                    where owner_id = {owner_id} and owner_type = {owner_type[2]}
                        """)
        await conn.execute(f"""update {owner_type[1].replace('id', 'statistics')}
                                  set {like_recommendations[0]} = {like_recommendations[0]} - 1
                                  where {owner_type[1]} = {owner_id}
                            """)
