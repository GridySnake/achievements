class CommunityWalletGoal:
    @staticmethod
    async def create_wallet_goal(community_id: str,
                                 data, conn):
        
        await conn.execute(f"""
                           insert into community_payment_goals (
                                goal_name, description, from_date, to_date, 
                                community_id, wallet_id, is_nessesarity, user_must_send, current_value, target_value, 
                                is_active) values(
                           '{data['goal_name']}', '{data['description']}', {data['from_date']}, {data['to_date']}, 
                           {community_id}, {data['wallet']}, true, ARRAY []::integer[], 0, {data['target_value']}, true)
                           """)

    @staticmethod
    async def close_wallet_goal(conn):
        await conn.execute(f"""
                    update community_payment_goals
                        set is_active = false
                    where current_value >= target_value
                """)

    @staticmethod
    async def get_payment_goal(community_id: str, conn,
                               is_active=True):
        """
        Get all goals as is_active
        :param community_id:
        :param is_active: boolean
                    is_active true or false
        :return:
        """
        community_id = int(community_id)
        payment_goals = await conn.fetch(f"""
                    select goal_name, payment_goal_id, target_value, 
                        current_value, from_date, to_date
                    from community_payment_goals
                    where community_id = {community_id}
                        and is_active = {is_active}
                """)
        return [dict(i) for i in payment_goals]


class Wallet:
    @staticmethod
    async def create_wallet(community_id: str,
                            data, conn):
        
        community_id = int(community_id)
        await conn.execute(f"""
            insert into community_wallet (
                                currency, responsible_users, is_active,  
                                community_id, wallet_name) values(
                           '{data['currency']}', ARRAY[{data['responsible_users']}], 
                           true, {community_id}, '{data['wallet_name']}')
                           
        """)
        wallet_id = await conn.fetchrow(f"""
                select max(wallet_id)
                from community_wallet
                where community_id = {community_id}
                """)
        return wallet_id['max']

    @staticmethod
    async def update_wallet_payment(wallet_id: str,
                                    payment_goal_id: str, conn):
        
        wallet_id = int(wallet_id)
        payment_goal_id = int(payment_goal_id)
        await conn.execute(f"""
            update community_wallet
                set payment_goals_id = array_append(payment_goals_id, {payment_goal_id})
            where wallet_id = {wallet_id} and {payment_goal_id} 
            not in (select unnest(payment_goals_id) 
                    from community_wallet 
                    where wallet_id = {wallet_id})
        """)

    @staticmethod
    async def deactivate_wallet(wallet_id, conn):
        wallet_id = int(wallet_id)
        await conn.execute(f"""
            update community_wallet
                set is_active = false,
                    deactivate_date = statement_timestamp()
            where wallet_id = {wallet_id}
        """)

    @staticmethod
    async def get_wallet(community_id: str, conn):
        community_id = int(community_id)
        wallets = await conn.fetch(f"""
            select wallet_name, wallet_id, currency
            from community_wallet
            where community_id = {community_id}
        """)
        return [dict(i) for i in wallets]
