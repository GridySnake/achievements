import asyncpg
from config.common import BaseConfig
import qrcode
import hashlib
from geopy.geocoders import Nominatim

connection_url = BaseConfig.database_url


class AchievementsGenerateData:
    @staticmethod
    async def data_for_group_drop_down_generate_achievements():
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch("""
                                           select distinct agc.condition_group_id as group_id, acg.achi_condition_group_name as group_name
                                           from achi_generate_conditions as agc
                                           left join achi_condition_groups as acg on agc.condition_group_id = acg.achi_condition_group_id
                                           order by agc.condition_group_id

                """)
        return achievements

    @staticmethod
    async def data_for_drop_downs_generate_achievements():
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch("""
                                           select agc.condition_group_id as group_id, acg.achi_condition_group_name as group_name, 
                                           aap1.aggregate_id, aap1.aggregate_name, aap.parameter_id, aap.parameter_name, 
                                           es.service_id, es.service_name
                                           from achi_generate_conditions as agc
                                           left join achi_aggregate_parameters aap on agc.parameter_id = aap.parameter_id
                                           left join achi_aggregate_parameters aap1 on agc.aggregate_id = aap1.aggregate_id
                                           left join achi_condition_groups as acg on agc.condition_group_id = acg.achi_condition_group_id
                                           left join external_services as es on agc.service_id = es.service_id

            """)
        return achievements


class AchievementsGetInfo:
    @staticmethod
    async def get_users_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        achievement = await conn.fetch(f"""
                                            select a.achievement_id, a.name
                                            from achievements as a
                                            right join (select unnest(achievements_id) as achievements_id from users_information where user_id = {user_id}) as u on u.achievements_id = a.achievement_id
            """)
        return achievement

    @staticmethod
    async def get_users_desire_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
                                            select a.achievement_id, a.name
                                             from achievements as a
                                             right join 
                                             (
                                                 select unnest(achievements_desired_id) as achievements_desired_id 
                                                 from users_information
                                                 where user_id = {user_id}
                                             ) as u on u.achievements_desired_id = a.achievement_id
                                            """)
        return achievements

    @staticmethod
    async def get_users_approve_achievements(user_id: str, user_active: str = None):
        conn = await asyncpg.connect(connection_url)
        if user_active is not None:
            achievement = await conn.fetch(f"""
                                               select a.achievement_id, a.name, COUNT(aa.user_passive_id) as approve
                                                from achievements as a
                                                right join 
                                                (
                                                    select unnest(achievements_desired_id) as achievements_desired_id 
                                                    from users_information 
                                                    where user_id = {user_id}
                                                ) as u 
                                                on u.achievements_desired_id = a.achievement_id
                                                left join approve_achievements as aa on aa.achievement_id = a.achievement_id and aa.user_active_id = {user_active}
                                                right join achi_conditions as ac on ac.condition_id = any(a.conditions) and ac.achi_condition_group_id = 7
                                                where a.achievement_id is not null
                                                group by a.achievement_id, a.name
                            """)
        else:
            achievement = await conn.fetch(f"""
                                                select a.achievement_id, a.name
                                                from achievements as a
                                                right join (select unnest(achievements_desired_id) as achievements_desired_id 
                                                from users_information where user_id = {user_id}) as u 
                                                on u.achievements_desired_id = a.achievement_id
                                                right join achi_conditions as ac on ac.condition_id = any(a.conditions) and ac.achi_condition_group_id = 7
                                                where a.achievement_id is not null
                """)
        return achievement

    @staticmethod
    async def get_achievement_info(achievement_id: str):
        conn = await asyncpg.connect(connection_url)
        achievement = await conn.fetchrow(f"""
                                            select a.achievement_id, a.name, a.description, c.aggregation, c.parameter_id, 
                                            c.value, g.achi_condition_group_id, g.achi_condition_group_name, a.created_date, 
                                            a.new, u.name as u_name, u.surname as u_surname, u.user_id, c.geo, c.condition_id,
                                            s.sphere_name, s.subsphere_name
                                            from achi_conditions as c
                                            right join (select achievement_id, unnest(conditions) as conditions, name, user_id, description, created_date, new, subsphere_id from achievements) as a on a.conditions::integer = c.condition_id
                                            left join achi_condition_groups as g on g.achi_condition_group_id = c.achi_condition_group_id
                                            left join users_information as u on a.user_id = u.user_id 
                                            left join spheres s on a.subsphere_id = s.subsphere_id
                                            where a.achievement_id = {achievement_id}
            """)
        return achievement

    @staticmethod
    async def get_achievement_by_condition_id(condition_id: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
                select a.achievement_id, a.name, c.value, c.geo
                from achi_conditions as c
                left join (select achievement_id, name, unnest(conditions) as conditions from achievements) as a on a.conditions::integer = c.condition_id
                where c.condition_id = {condition_id}
                """)
        return achievements

    @staticmethod
    async def get_achievement_by_condition_value(value: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
            select a.name, c.value, c.geo, c.achi_condition_group_id
            from achi_conditions as c
            left join (select name, unnest(conditions) as conditions from achievements) as a on a.conditions::integer = c.condition_id
            where c.value = '{value}'
            """)
        return achievements

    @staticmethod
    async def get_achievement_by_condition_parameter(parameter: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
                select a.achievement_id, a.name, c.value, c.geo, c.achi_condition_group_id
                from achi_conditions as c
                left join (select achievement_id, name, unnest(conditions) as conditions from achievements) as a on a.conditions::integer = c.condition_id
                where c.parameter_id = '{parameter}'
                """)
        return achievements

    @staticmethod
    async def get_created_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
        select achievement_id, name, a.description, achievement_qr, s.sphere_name, s.subsphere_name, c.community_name,
            co.course_name
        from achievements as a
        left join spheres as s on a.subsphere_id = s.subsphere_id
        left join communities as c on a.user_id = any(c.community_owner_id) and user_type = 1
        left join courses as co on co.course_owner_id = a.user_id and user_type = 2
        where (a.user_id = {user_id} and user_type = 0) or c.community_name is not null or co.course_name is not null
        """)
        return achievements

    @staticmethod
    async def get_reached_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
            select achievement_id, a.name, a.description, s.sphere_name, s.subsphere_name
            from (select user_id, unnest(achievements_id) as achievements_id from users_information) as u
            inner join achievements as a on u.achievements_id = a.achievement_id
            left join spheres s on a.subsphere_id = s.subsphere_id
            where u.user_id = {user_id}
            """)
        return achievements

    @staticmethod
    async def get_suggestion_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
            select achievement_id, a.user_id, a.user_type, a.name as title, a.description, a.created_date, a.new, u.name, u.surname,
            s.sphere_name, s.subsphere_name, c.community_name, c.community_owner_id, co.course_name
            from achievements as a
            left join users_information as u on u.user_id = a.user_id and a.user_type = 0
            left join communities as c on a.user_id = c.community_id and a.user_type = 1
            left join courses as co on co.course_id = a.user_id and a.user_type = 2
            left join spheres s on a.subsphere_id = s.subsphere_id
            left join users_information as u1 on a.achievement_id = any(u1.achievements_id) or a.achievement_id = any(u1.achievements_desired_id)
            where ({user_id} <> any(c.community_owner_id) or c.community_owner_id is null) and
                  ({user_id} <> co.course_owner_id or co.course_owner_id is null) and
                  (u1.user_id is null or u1.user_id <> {user_id}) and
                  u.user_id <> {user_id}
            """)
        return achievements


class AchievementsGiveVerify:
    @staticmethod
    async def give_achievement_to_user(achievement_id: str, user_id: str):
        conn = await asyncpg.connect(connection_url)
        try:
            await conn.execute(f"""
                                update users_information
                                set achievements_id = array_append(achievements_id, {achievement_id})
                                where user_id = {user_id} and {achievement_id} not in (
                                        select unnest(achievements_id) from users_information where user_id = {user_id})
            """)
        except:
            return 1

    @staticmethod
    async def update_user_info_achievements(user_id: str):
        conn = await asyncpg.connect(connection_url)
        data = await conn.fetch(f"""
                                select a.achievement_id, c.parameter, c.value
                                from (select achievement_id, unnest(conditions) as conditions from achievements) as a
                                inner join achi_conditions as c on text(c.condition_id) = a.conditions
                                where achi_condition_group_id = 0  and a.achievement_id not in (select unnest(achievements_id) as achievements_id from users_information where user_id = {user_id})
        """)
        for i in data:
            if i['value'].isdigit():
                await conn.execute(f"""
                                    update users_information
                                    set achievements_id = array_append(achievements_id, {i['achievement_id']})
                                    where user_id = {user_id} and {i['parameter']} = {i['value']} and {i['achievement_id']} not in (
                                        select unnest(achievements_id) from users_information where user_id = {user_id})
                                    """)
            else:
                await conn.execute(f"""
                                    update users_information
                                    set achievements_id = array_append(achievements_id, {i['achievement_id']})
                                    where user_id = {user_id} and {i['parameter']} = '{i['value']}' and {i['achievement_id']} not in (
                                        select unnest(achievements_id) from users_information where user_id = {user_id})
                                   """)

    @staticmethod
    async def qr_verify(user_id: str, value: str):
        conn = await asyncpg.connect(connection_url)
        try:
            achi_id = await conn.fetchrow(f"""
                            select a.achievement_id
                            from achi_conditions as c
                            inner join (select achievement_id, unnest(conditions) as conditions from achievements) as a on a.conditions::integer = c.condition_id
                            where achi_condition_group_id = 1 and value = '{value}'
            """)
            await conn.execute(f"""
                                update users_information
                                set achievements_id = array_append(achievements_id, {achi_id['achievement_id']})
                                where user_id = {user_id} and {achi_id['achievement_id']} not in (
                                        select unnest(achievements_id) from users_information where user_id = {user_id})
            """)
        except:
            return 1

    @staticmethod
    async def location_verify(user_id: str, value: str):
        conn = await asyncpg.connect(connection_url)
        achi_id = await conn.fetchrow(f"""
                            select a.achievement_id
                            from achi_conditions as c
                            inner join (select achievement_id, unnest(conditions) as conditions from achievements) as a on a.conditions::integer = c.condition_id
                            where achi_condition_group_id = 2 and value = '{value}'
            """)
        await conn.execute(f"""
                                update users_information
                                set achievements_id = array_append(achievements_id, {achi_id['achievement_id']})
                                where user_id = {user_id} and {achi_id['achievement_id']} not in (
                                        select unnest(achievements_id) from users_information where user_id = {user_id})
            """)

    @staticmethod
    async def chess_verify(user_id: str, achievement_id: str):
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
                               update users_information
                               set achievements_id = array_append(achievements_id, {achievement_id})
                               where user_id = {user_id} and {achievement_id} not in (
                                       select unnest(achievements_id) from users_information where user_id = {user_id})
            """)

    @staticmethod
    async def desired_to_reached_achievement(user_id: str):
        conn = await asyncpg.connect(connection_url)
        achievements = await conn.fetch(f"""
                                select a.achievement_id as achievement_id
                                from (select achievement_id, unnest(conditions) as conditions from achievements) as a
                                left join achi_conditions as c on c.condition_id = a.conditions::integer
                                left join (
                                    select a.achievement_id, COUNT(aa.user_passive_id) as approve
                                from achievements as a
                                right join 
                                (
                                    select unnest(achievements_desired_id) as achievements_desired_id 
                                    from users_information 
                                    where user_id = {user_id}
                                ) as u 
                                on u.achievements_desired_id = a.achievement_id
                                left join approve_achievements as aa on aa.achievement_id = a.achievement_id
                                group by a.achievement_id) as q on q.achievement_id = a.achievement_id
                                right join (
                                    select unnest(achievements_desired_id) as achievements_desired_id 
                                    from users_information 
                                    where user_id = {user_id}
                                ) as u 
                                on u.achievements_desired_id = a.achievement_id
                                where c.achi_condition_group_id = 7 and c.value::integer <= q.approve
                   """)
        for i in achievements:
            await conn.execute(f"""
                                  update users_information
                                  set achievements_id = array_append(achievements_id, {i['achievement_id']})
                                  where user_id = {user_id} and {i['achievement_id']} not in (select unnest(achievements_id) as achievements_id from users_information where user_id = {user_id})
            """)
            await conn.execute(f"""
                                    update users_information
                                    set  achievements_desired_id = achievements_desired_id[:(select array_position(achievements_desired_id, {i['achievement_id']})
                                    from users_information						 
                                    WHERE user_id = {user_id})-1] ||
                                    achievements_desired_id[(select array_position(achievements_desired_id, {i['achievement_id']})
                                    from users_information
                                    WHERE user_id = {user_id})+1:]
                                    WHERE user_id = {user_id}
            """)


class AchievementsDesireApprove:
    @staticmethod
    async def desire_achievement(user_id: str, user_type: int, achievement_desire_id: str):
        conn = await asyncpg.connect(connection_url)
        if user_type == 0:
            table = 'users_information'
            column = 'user_id'
        elif user_type == 1:
            table = 'communities'
            column = 'community_id'
        elif user_type == 2:
            table = 'courses'
            column = 'course_id'
        await conn.execute(f"""
                               update {table}
                                   set achievements_desired_id = array_append(achievements_desired_id, {achievement_desire_id})
                                   where {column} = {user_id}
                                        and {achievement_desire_id} not in (
                                   select unnest(achievements_desired_id) 
                                   from {table} 
                                   where {column} = {user_id})
                           """)

    @staticmethod
    async def is_desire(user_id: str, achievement_desire_id: str):
        conn = await asyncpg.connect(connection_url)
        data = await conn.fetchrow(f"""
                                       select count(achievements_desired_id)
                                       from (select unnest(achievements_desired_id) as achievements_desired_id from users_information where user_id = {user_id}) as u 
                                       where u.achievements_desired_id = {achievement_desire_id}
               """)
        if data['count'] > 0:
            result = True
        else:
            result = False
        return result

    @staticmethod
    async def approve_achievement(user_active_id: str, user_passive_id: str, achievement_id: str):
        conn = await asyncpg.connect(connection_url)
        id = await conn.fetchrow(f"""
                        select max(approvement_id)
                        from approve_achievements
                        """)
        id = dict(id)['max']
        if id is not None:
            id = int(id) + 1
        else:
            id = 0
        await conn.execute(f"""
                               insert into approve_achievements (approvement_id, user_active_id, user_passive_id, achievement_id) values (
                               {id}, {user_active_id}, {user_passive_id}, {achievement_id})
                       """)


class AchievementsCreate:
    @staticmethod
    async def create_achievement(user_id: str, user_type: int, data):
        # todo: убрать параметр, иногда только по агрегации создается
        conn = await asyncpg.connect(connection_url)
        id_achi = await conn.fetch(f"""
                select max(achievement_id)
                from achievements
                """)
        id_achi = dict(id_achi[0])['max']
        if id_achi is not None:
            id_achi = int(id_achi) + 1
        else:
            id_achi = 0
        id_condi = await conn.fetch(f"""
                            select max(condition_id)
                            from achi_conditions
                            """)
        id_condi = dict(id_condi[0])['max']
        if id_condi is not None:
            id_condi = int(id_condi) + 1
        else:
            id_condi = 0
        await conn.execute(f"""
                               insert into achi_conditions (condition_id, aggregation_id, parameter_id, value, 
                                    achi_condition_group_id, geo) values(
                                {id_condi}, {data['select_aggregation']}, {data['select_parameter']}, 
                                '{data['value']}', {data['select_group']}, {data['geo']})
                            """)
        if data['achievement_qr'] == 'null':
            await conn.execute(f"""
                                   insert into achievements (achievement_id, user_id, user_type, name, description, 
                                        conditions, created_date, new, achievement_qr, sphere_id, subsphere_id) values(
                                        {id_achi}, {user_id}, {user_type}, '{data['name']}', '{data['description']}',
                                        ARRAY[{id_condi}], statement_timestamp(), true, {data['achievement_qr']}, 
                                        {data['sphere']}, {data['select_subsphere']})
                                """)
        else:
            await conn.execute(f"""
                                   insert into achievements (achievement_id, user_id, user_type, name, description, 
                                        conditions, created_date, new, achievement_qr, sphere_id, subsphere_id) values(
                                        {id_achi}, {user_id}, {user_type}, '{data['name']}', '{data['description']}',
                                        ARRAY[{id_condi}], statement_timestamp(), true, '{data['achievement_qr']}', 
                                        {data['sphere']}, {data['select_subsphere']})
                                """)
        # elif int(data['select_group']) == 31 and data['name'] != '' and data['description'] != '' and data['value'] != '' and data['select_service'] == '0':
        #     parameter = str(data['select_service'] + '-' + data['chess_parameter_global'] + '-' + data['chess_parameter_local_profile'] + '-' + data['chess_parameter_local_last'] + '-' + data['chess_parameter_local_chess'] + '-' + data['chess_parameter_local_equal'])
        #     await conn.execute(f"""
        #                             insert into achi_conditions (condition_id, parameter, value, achi_condition_group_id) values(
        #                             {id_condi}, '{parameter}', '{data['value']}', {data['select_group']})
        #                             """)
        #     await conn.execute(f"""
        #                             insert into achievements (achievement_id, user_id, user_type, name, description,
        #                                     conditions, created_date, new, sphere_id, subsphere_id) values(
        #                             {id_achi}, {user_id}, {user_type}, '{data['name']}', '{data['description']}',
        #                             ARRAY['{id_condi}'], statement_timestamp(), true, {data['sphere']},
        #                                     {data['select_subsphere']})
        #                             """)

