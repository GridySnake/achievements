class CommunityGetInfo:
    # Recommendation system will be here!!!
    @staticmethod
    async def get_some_communities(user_id, conn):
        user_id = int(user_id)
        communities = await conn.fetch(f"""
            select c.community_id, c.community_name
            from communities as c
            where {user_id} not in (select unnest(user_id)
                                   from communities 
                                   where c.community_id = community_id)
            limit (10)
        """)
        return communities

    @staticmethod
    async def get_community_info_by_value(community_id: str, value: str, conn):
        community = await conn.fetchrow(f"""
                                         select {value} 
                                         from community_statistics
                                         where community_id = {community_id}
                                     """)
        return community[value]

    @staticmethod
    async def get_user_communities(user_id, conn, own):
        if own:
            operator = '= ANY'
        else:
            operator = '<> ALL'
        communities = await conn.fetch(f"""
                                          select c.community_id, c.community_name, 
                                                s.sphere_name, s.subsphere_name, i.href
                                          from communities as c
                                          right join (
                                                      select unnest(community_id) as community_id 
                                                      from users_information 
                                                      where user_id={user_id}
                                                      ) as u 
                                                      on u.community_id = c.community_id
                                          left join (
                                                        select c.community_id, array_agg(s.subsphere_name) as subsphere_name, 
                                                        array_agg(s.sphere_name) as sphere_name
                                                        from communities as c
                                                            left join spheres s 
                                                                on s.subsphere_id = any(c.subsphere_id)
                                                        group by c.community_id
                                                    ) s on c.community_id = s.community_id
                                          left join images as i 
                                                on i.image_id = c.image_id[array_upper(c.image_id, 1)] 
                                                    and i.image_type = 'community'
                                          where {user_id} {operator}(c.community_owner_id)
                                          """)
        return [dict(i) for i in communities]

    @staticmethod
    async def get_user_owner_communities(user_id, conn):
        communities = await conn.fetch(f"""
                                           select c.community_id, c.community_name, s.sphere_name, s.subsphere_name
                                           from (
                                                 select community_id, community_name, 
                                                 unnest(community_owner_id) as community_owner_id 
                                                 from communities) as c
                                           right join (
                                                       select unnest(community_owner_id) as community_owner_id 
                                                       from users_information 
                                                       where user_id = {user_id}
                                                       ) as u on u.community_owner_id = c.community_owner_id
                                           left join (
                                                        select c.community_id, array_agg(s.subsphere_name) as subsphere_name, 
                                                        array_agg(s.sphere_name) as sphere_name
                                                        from communities as c
                                                        left join spheres s on s.subsphere_id = any(c.subsphere_id)
                                                        group by c.community_id
                                                    ) s on c.community_id = s.community_id
                                           where c.community_id is not null
                                           """)
        return [dict(i) for i in communities]

    @staticmethod
    async def get_community_info(community_id, conn):
        community = await conn.fetchrow(f"""
                                           select c.community_id, c.community_name, c.community_type,
                                                  c.community_bio, unnest(c.conditions) as condition_id,
                                                  c.created_date, i.href
                                           from communities as c
                                           left join images as i
                                           on i.image_id = c.image_id[array_upper(c.image_id, 1)]
                                                and i.image_type = 'community'
                                           where c.community_id = {community_id}
                                           """)
        return dict(community)
    # async def get_community_info(community_id, conn):
    #     community = await conn.fetchrow(f"""
    #                                        select u.user_id, u.name, u.surname, c.community_id,
    #                                                 c.community_name, c.community_type, c.community_bio,
    #                                                 c.condition_id, c.created_date, i.href, c.community_owner_id
    #                                        from users_information as u
    #                                        right join (select community_id, community_name, community_type,
    #                                                         unnest(user_id) as user_id, community_bio,
    #                                                         unnest(conditions) as condition_id,
    #                                                         created_date, image_id,
    #                                                         unnest(community_owner_id) as community_owner_id
    #                                                     from communities) as c
    #                                                     on c.user_id = u.user_id
    #                                        left join images as i
    #                                        on i.image_id = c.image_id[array_upper(c.image_id, 1)]
    #                                             and i.image_type = 'community'
    #                                        where c.community_id = {community_id}
    #                                        """)
    #     return [dict(i) for i in community]

    @staticmethod
    async def user_in_community(community_id: str, user_id: str, conn):
        in_community = await conn.fetchrow(f"""
                                            select case when {user_id} = any(c.user_id) then true else false end 
                                                as in_community
                                            from  communities as c
                                            where c.community_id = {community_id}
                                        """)
        return in_community['in_community']

    @staticmethod
    async def get_community_owners(community_id, conn):
        community = await conn.fetch(f"""
            select u.user_id, u.name, u.surname
            from users_information as u
            right join (select community_id, unnest(community_owner_id) as owner_id
                         from communities) as c 
                         on c.owner_id = u.user_id
            where c.community_id = {community_id}
        """)
        return [dict(i) for i in community]

    @staticmethod
    async def get_community_participants(community_id, conn):
        community = await conn.fetch(f"""
                                            select u.user_id, u.name, u.surname
                                            from users_information as u
                                            right join (select community_id, unnest(user_id) as user_id
                                                         from communities) as c on c.user_id = u.user_id
                                            where c.community_id = {community_id}
                                        """)
        return [dict(i) for i in community]

    @staticmethod
    async def get_generate_conditions(conn):
        conditions = await conn.fetch(f"""
                                    select condition_id, condition_name, condition_description, community_type
                                    from community_conditions_generate
                                """)
        return conditions

    @staticmethod
    async def user_requests(user_id: str, conn):
        conditions = await conn.fetch(f"""
                                        select community_id, community_name
                                        from communities
                                        where {user_id} = any(requests) 
                                        and request_statuses[array_position(requests, {user_id})] = 1
                                    """)
        return conditions

    @staticmethod
    async def is_owner(user_id: str, community_id: str, conn):
        owner = await conn.fetch(f"""select case when count(*) > 0 then true else false end as owner
                                     from communities as com
                                     left join users_information ui on ui.user_id = any(com.community_owner_id)
                                     where com.community_id = {community_id} and ui.user_id = {user_id}
                                 """)
        return owner['owner']

    @staticmethod
    async def get_community_conditions(user_id: str, community_id: str, conn):
        conditions = await conn.fetch(f"""select c.task, c.condition_value, gc.condition_name, i.href, 
                                            gc.generate_condition_id, case when {user_id} = any(c.users_approved)
                                            then true else false end as approved, case when {user_id} = 
                                                cl.user_id then true else false end as cl_send, case when {user_id} = 
                                                int.user_id then true else false end as int_send
                                            from communities as com
                                            left join conditions as c on
                                                c.condition_id = any(com.conditions)
                                            left join generate_conditions gc 
                                                on c.generate_condition_id = gc.generate_condition_id
                                            left join images as i on i.image_id = c.image_id
                                            left join cover_letters as cl on cl.cover_letter_id = any(com.cover_letters)
                                            left join interviews as int on int.interview_id = any(com.interviews)
                                            where com.community_id = {community_id} and 
                                                ({user_id} <> any(com.conditions_approved) or 
                                                com.conditions_approved = array[]::integer[])
                                    """)
        return [dict(i) for i in conditions]


class CommunityAvatarAction:
    @staticmethod
    async def save_community_avatar_url(community_id, url, conn):
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
    async def leave_join(community_id, method, user_id, conn):
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
    async def add_member(community_id: str, users: list, status: list, conn):
        await conn.execute(f"""
                               update communities
                                    set requests = array_cat(requests, array[{users}]),
                                        request_statuses = array_cat(requests, {status})
                                    where community_id = {community_id}
                            """)

    @staticmethod
    async def remove_member(community_id: str, users: list, conn):
        for i in users:
            await conn.execute(f"""
                                   update communities
                                        set user_id = array_remove(user_id, {i})
                                        where community_id = {community_id}
                                """)

    @staticmethod
    async def accept_decline_request(user_id: str, action: int, community_id: str, conn):
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
    async def create_community(user_id, data, conn):
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
                               insert into communities (community_id, community_type, community_name, community_bio, 
                                    user_id, community_owner_id, created_date, image_id, conditions,
                                    sphere_id, subsphere_id)
                               values({id}, '{data['community_type']}', '{data['name']}', '{data['bio']}', 
                                    array[{user_id}], array[{user_id}], statement_timestamp(), ARRAY []::integer[], 
                                    ARRAY []::integer[], array[{data['sphere']}],
                                array[{data['select_subsphere']}])
                           """)
        await conn.execute(f"""
                                update users_information 
                                set community_id = array_append(community_id, {id}),
                                    community_owner_id = array_append(community_owner_id, {id})
                                where user_id = {user_id}
                            """)
        await conn.execute(f"""
                                insert into chats (chat_id, chat_type, participants, owner_id) values(
                                {chat_id}, 2, array[{user_id}], {id})
                            """)
        await conn.execute(f"""
                               insert into community_statistics (community_id, participants, rating, likes, comments, 
                                    reach_achievements, create_achievements, create_courses) values(
                                    {id}, 1, 0, 0, 0, 0, 0, 0)
                            """)
        await conn.execute(f"""
                               insert into likes (owner_id, owner_type, users_liked_id, users_liked_type, 
                                   action_datetime) values({id}, 1, array[]::integer[], array[]::integer[],
                                   array[]::timestamptz[])
                            """)
        await conn.execute(f"""
                               insert into dislikes (owner_id, owner_type, users_disliked_id, users_disliked_type, 
                                   action_datetime) values({id}, 1, array[]::integer[], array[]::integer[],
                                   array[]::timestamptz[])
                            """)
        await conn.execute(f"""
                               insert into recommendations (owner_id, owner_type, users_recommend_id, 
                                    users_recommend_type, action_datetime) values({id}, 1, array[]::integer[], 
                                    array[]::integer[], array[]::timestamptz[])
                            """)
        return id

    @staticmethod
    async def create_community_info_conditions(community_id: str, data: dict, conn):
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
                                           generate_condition_id, users_approved)
                                           values ({condition_id}, '{data['task'][i]}', {data['answers'][i]},
                                           '{data['condition_value'][i]}', null, {data['condition_id'][i]}, 
                                           array[]::integer)
                                    """)
            elif data['task'][i] == 'null' and data['condition_value'][i] != 'null':
                await conn.execute(f"""
                                       insert into conditions (condition_id, task, answer, condition_value, image_id, 
                                           generate_condition_id, users_approved)
                                           values ({condition_id}, {data['task'][i]}, {data['answers'][i]},
                                           '{data['condition_value'][i]}', null, {data['condition_id'][i]}, 
                                           array[]::integer)
                                    """)
            elif data['task'][i] == 'null' and data['condition_value'][i] == 'null':
                await conn.execute(f"""
                                       insert into conditions (condition_id, task, answer, condition_value, image_id, 
                                           generate_condition_id, users_approved)
                                           values ({condition_id}, {data['task'][i]}, {data['answers'][i]},
                                           {data['condition_value'][i]}, null, {data['condition_id'][i]}, 
                                           array[]::integer)
                                    """)
            elif data['task'][i] != 'null' and data['answers'][i] != 'null' and data['condition_value'][i] != 'null' \
                    and data['images'][i] == 'null':
                await conn.execute(f"""
                                       insert into conditions (condition_id, task, answer, condition_value, image_id, 
                                           generate_condition_id, users_approved)
                                           values ({condition_id}, '{data['task'][i]}', '{data['answers'][i]}',
                                           '{data['condition_value'][i]}', null, {data['condition_id'][i]}, 
                                           array[]::integer)
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
                                           generate_condition_id, users_approved)
                                           values ({condition_id}, '{data['task'][i]}', {data['answers'][i]},
                                           '{data['condition_value'][i]}', {image_id}, {data['condition_id'][i]}, 
                                           array[]::integer)
                                    """)
            await conn.execute(f"""
                                   update communities
                                        set conditions = array_append(conditions, {condition_id})
                                    where community_id = {community_id}
                                """)
