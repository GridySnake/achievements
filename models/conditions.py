class ConditionsGetInfo:

    @staticmethod
    async def get_conditions(user_id: str, owner_id: str, owner_type: list, conn):
        conditions = await conn.fetch(f"""select c.condition_id, c.task, c.answer, c.condition_value, gc.condition_name
                                            from {owner_type[0]} as ow
                                            left join conditions as c 
                                                on c.condition_id = any(ow.conditions)
                                            left join generate_conditions as gc 
                                                on c.generate_condition_id = gc.generate_condition_id
                                            left join images as i on i.image_id = c.image_id
                                            where ow.{owner_type[1]} = {owner_id} and ({user_id} <> 
                                                any(c.users_approved) or c.users_approved = array[]::integer[])
                                    """)
        return conditions

    @staticmethod
    async def is_follower(user_active_id: str, user_passive_id: str, parameter: str, conn):
        if parameter == 'followings':
            user = user_active_id
            user_active_id = user_passive_id
            user_passive_id = user
        follower = await conn.fetch(f"""select case when count(distinct status_id) = 1 then true
                                          else false
                                          end as follower
                                          from
                                          (select user_id, unnest(users_id) as users_id, unnest(status_id) as 
                                              status_id from subscribes where status_id = 1) as f
                                          inner join users_information as u on u.user_id = f.users_id
                                          where f.user_id = {user_active_id}
                                              and u.user_id = {user_passive_id} and status_id = 1
                                        """)
        return follower['follower']

    @staticmethod
    async def get_condition_user_statistics(user_id: str, condition_name: str, condition_value: str, conn):
        statistics = await conn.fetchrow(f"""select case when {condition_name} >= {condition_value} then true
                                             else false end as result
                                             from user_statistics
                                             where user_id = {user_id}
                                        """)
        return statistics['result']

    @staticmethod
    async def get_data_for_condition_test(user_id: str, condition_id: str, conn):
        email = await conn.fetchrow(f"""
                                        select u.email
                                        from users_main as u
                                        where user_id = {user_id}
                                    """)
        answer = await conn.fetchrow(f"""
                                         select c.answer
                                         from conditions as c
                                         where c.condition_id={condition_id}
                                     """)
        return [email['email'], answer['answer']]

    @staticmethod
    async def is_allowed_communicate_by_conditions(user_active_id: str, user_passive_id: str, owner_table: str,
                                                   owner_column: str, conn):
        """
        :param user_active_id: str
        :param user_passive_id: str
        :param owner_table: str
        :param owner_column: str
        :return: allow: bool
        """
        allow = await conn.fetchrow(f"""
                                        select case when count(*) = 1 then true
                                        else false
                                        end as allow
                                        from {owner_table} as ow
                                        where ow.{owner_column} = {user_passive_id} and 
                                            {user_active_id} = any(ow.conditions_approved)
                                    """)
        allow = allow['allow']
        return allow

    @staticmethod
    async def get_cover_letters(receiver_id: str, receiver_type: int, conn):
        cover_letters = await conn.fetch(f"""
                                             select cl.user_id, ui.name, ui.surname, cl.letter_text, cl.letter_href
                                             from cover_letters as cl
                                             left join users_information ui on cl.user_id = ui.user_id
                                             where receiver_id = {receiver_id} and receiver_type = {receiver_type} and
                                                status = 0
                                             order by cl.send_datetime desc
                                         """)
        return [dict(i) for i in cover_letters]

    @staticmethod
    async def get_interviews_requests(sender_id: str, sender_type: int, conn):
        interviews = await conn.fetch(f"""
                                          select int.user_id, ui.name, ui.surname, int.send_datetime
                                          from interviews as int
                                          left join users_information ui on int.user_id = ui.user_id
                                          where sender_id = {sender_id} and sender_type = {sender_type} and status = 0
                                            and href is null
                                          order by int.send_datetime desc
                                        """)
        return interviews

    @staticmethod
    async def is_send(user_id: str, sender_id: str, sender_type: list, conn):
        send = await conn.fetchrow(f"""
                                       select case when count(*) > 0 then true else false end as send
                                       from interviews
                                       where sender_id = {sender_id} and sender_type = {sender_type[2]} 
                                        and user_id = {user_id}
                                    """)
        return send['send']

    @staticmethod
    async def get_interviews_future(sender_id: str, sender_type: int, conn):
        interviews = await conn.fetch(f"""
                                          select int.user_id, ui.name, ui.surname, int.href, int.interview_datetime, 
                                            int.send_datetime
                                          from interviews as int
                                          left join users_information ui on int.user_id = ui.user_id
                                          where sender_id = {sender_id} and sender_type = {sender_type} and status = 0
                                            and int.href is not null
                                          order by int.send_datetime desc
                                      """)
        return interviews


class ConditionsInsertCheck:
    @staticmethod
    async def approve_condition(user_id: str, condition_id: list, conn):
        await conn.execute(f"""
                               update conditions as c
                               set users_approved = array_append(users_approved, {user_id})
                               where c.condition_id in ({','.join(condition_id)})
                           """)

    @staticmethod
    async def give_access(user_active_id: str, owner_id: str, owner_type: list, conn):
        await conn.execute(f"""
                               update {owner_type[0]} as ow
                               set conditions_approved = array_append(conditions_approved, {user_active_id})
                               where ow.{owner_type[1]} = {owner_id} and ({user_active_id} <> any(conditions_approved) 
                                    or conditions_approved = array[]::integer[])
                            """)

    @staticmethod
    async def request_interview(user_id: str, owner_id: str, owner_type: list, condition_id: int, conn):
        interview_id = await conn.fetchrow("""select max(interview_id) from interviews""")
        interview_id = dict(interview_id)['max']
        if interview_id:
            interview_id += 1
        else:
            interview_id = 0
        await conn.execute(f"""
                               insert into interviews (interview_id, sender_id, sender_type, user_id, send_datetime, 
                                    href, interview_datetime, status) values ({interview_id}, {owner_id}, 
                               {owner_type[2]}, {user_id}, statement_timestamp(), null, null,
                               0)
                           """)
        await conn.execute(f"""
                               update {owner_type[0]} 
                               set interviews = array_append(interviews, {interview_id})
                               where {owner_type[1]} = {owner_id}
                            """)
        await conn.execute(f"""
                               update conditions
                               set interviews = array_append(interviews, {interview_id})
                               where condition_id = {condition_id}
                            """)

    @staticmethod
    async def send_cover_letter(user_id: str, owner_id: str, owner_type: list, data: dict, condition_id: int, conn):
        cl_id = await conn.fetchrow("""select max(cover_letter_id) from cover_letters""")
        cl_id = dict(cl_id)['max']
        if cl_id:
            cl_id += 1
        else:
            cl_id = 0
        if data['letter_text'] == 'null':
            await conn.execute(f"""
                                   insert into cover_letters (cover_letter_id, user_id, receiver_id, receiver_type, 
                                   send_datetime, letter_text, letter_href) values ({cl_id}, {user_id}, {owner_id}, 
                                   {owner_type[2]}, statement_timestamp(), {data['letter_text']}, 
                                   '{data['letter_href']}')
                                """)
        elif data['letter_href'] == 'null':
            await conn.execute(f"""
                                   insert into cover_letters (cover_letter_id, user_id, receiver_id, receiver_type, 
                                   send_datetime, letter_text, letter_href) values ({cl_id}, {user_id}, {owner_id}, 
                                   {owner_type[2]}, statement_timestamp(), '{data['letter_text']}', 
                                   {data['letter_href']})
                               """)
        else:
            await conn.execute(f"""
                                   insert into cover_letters (cover_letter_id, user_id, receiver_id, receiver_type, 
                                   send_datetime, letter_text, letter_href) values ({cl_id}, {user_id}, {owner_id}, 
                                   {owner_type[2]}, statement_timestamp(), '{data['letter_text']}', 
                                   '{data['letter_href']}')
                                """)
        await conn.execute(f"""
                               update {owner_type[0]} 
                               set cover_letters = array_append(cover_letters, {cl_id})
                               where {owner_type[1]} = {owner_id}
                            """)
        await conn.execute(f"""
                               update conditions
                               set cover_letters = array_append(cover_letters, {cl_id})
                               where condition_id = {condition_id}
                            """)

    @staticmethod
    async def accept_decline_cover_letter(user_id: str, receiver_id: str, receiver_type: list, status: int, conn):
        await conn.execute(f"""
                               update cover_letters
                               set status = {status}
                               where receiver_id = {receiver_id} and receiver_type = {receiver_type[2]} 
                                and user_id = {user_id}
                            """)
        if status == 1:
            await conn.execute(f"""
                                   update conditions as c
                                   set users_approved = array_append(c.users_approved, {user_id})
                                   from cover_letters as cl 
                                   where cl.receiver_id = {receiver_id} and cl.receiver_type = {receiver_type[2]} 
                                        and cl.user_id = {user_id} and cl.cover_letter_id = any(c.cover_letters)
                                """)
            conditions = await ConditionsGetInfo.get_conditions(user_id=user_id, owner_id=receiver_id,
                                                                owner_type=receiver_type)
            if not conditions:
                await ConditionsInsertCheck.give_access(user_active_id=user_id, owner_id=receiver_id,
                                                        owner_type=receiver_type)
            elif len(conditions) == 1 and conditions[0]['condition_name'] == 'interview':
                await ConditionsInsertCheck.request_interview(user_id=user_id, owner_id=receiver_id,
                                                              owner_type=receiver_type)

    @staticmethod
    async def accept_decline_interview(user_id: str, sender_id: str, sender_type: list, status: int, conn):
        await conn.execute(f"""
                               update interviews
                               set status = {status}
                               where sender_id = {sender_id} and sender_type = {sender_type[2]} 
                                and user_id = {user_id}
                            """)
        if status == 1:
            await conn.execute(f"""
                                   update conditions as c
                                   set users_approved = array_append(c.users_approved, {user_id})
                                   from interviews as int 
                                   where int.sender_id = {sender_id} and int.sender_type = {sender_type[2]} 
                                        and int.user_id = {user_id} and int.interview_id = any(c.interviews)
                                """)
            conditions = await ConditionsGetInfo.get_conditions(user_id=user_id, owner_id=sender_id,
                                                                owner_type=sender_type)
            if not conditions:
                await ConditionsInsertCheck.give_access(user_active_id=user_id, owner_id=sender_id,
                                                        owner_type=sender_type)

    @staticmethod
    async def update_interview_info(sender_id: str, sender_type: list, data: dict, conn):
        await conn.execute(f"""
                               update interviews
                               set href = '{data['link']}',
                                interview_datetime = '{data['datetime']}'::timestamptz
                               where sender_id = {sender_id} and sender_type = {sender_type[2]} 
                                and user_id = {data['user_id']}
                            """)
