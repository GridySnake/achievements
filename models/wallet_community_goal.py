import asyncpg
from config.common import BaseConfig
connection_url = BaseConfig.database_url


class CommunityWalletGoal:
    @staticmethod
    async def create_wallet_goal(community_id: str,
                                 data):
        conn = await asyncpg.connect(connection_url)
        # wallet_id = await conn.fetch(f"""
        #                 select max(wallet_id)
        #                 from community_wallet
        #                 """)
        # if wallet_id is not None:
        #     wallet_id = int(wallet_id) + 1
        # else:
        #     wallet_id = 0

        # payment_goal_id = await conn.fetch(f"""
        #                 select max(payment_goal_id)
        #                 from community_payment_goals
        #                 """)
        # if payment_goal_id is not None:
        #     payment_goal_id = int(payment_goal_id) + 1
        # else:
        #     payment_goal_id = 0
        await conn.execute(f"""
                           insert into community_payment_goals (
                                goal_name, description, from_date, to_date, 
                                community_id, wallet_id, is_nessesarity, user_must_send, target_value, is_active) values(
                           '{data['name']}', '{data['description']}', {data['from_date']}, {data['to_date']}, 
                           {community_id}, {data['wallet_id']}, {data['is_nessesarity']}, ARRAY[{data['user_must_send']}], {data['target_value']}, true)
                           """)

    @staticmethod
    async def close_wallet_goal():
        conn = await asyncpg.connect(connection_url)
        await conn.execute(f"""
                    update community_payment_goals
                        set is_active = false
                    where current_value >= target_value
                """)

    @staticmethod
    async def get_payment_goal(community_id: str,
                               is_active=True):
        """
        Get all goals as is_active
        :param community_id:
        :param is_active: boolean
                    is_active true or false
        :return:
        """
        conn = await asyncpg.connect(connection_url)
        community_id = int(community_id)
        payment_goals = await conn.fetch(f"""
                    select goal_name, payment_goal_id, target_value, 
                        current_value, from_date, to_date
                    from community_payment_goals
                    where community_id = {community_id}
                        and is_active = {is_active}
                """)
        return payment_goals


class Wallet:
    @staticmethod
    async def create_wallet(community_id: str,
                            data):
        conn = await asyncpg.connect(connection_url)
        community_id = int(community_id)
        await conn.execute(f"""
            insert into community_wallet (
                                currency, responsible_users, is_active,  
                                community_id, wallet_name) values(
                           '{data['currency']}', ARRAY[{data['responsible_users']}], 
                           true, {community_id}, '{data['wallet_name']}')
                           
        """)

    @staticmethod
    async def update_wallet_payment(wallet_id: str,
                            payment_goal_id: str):
        conn = await asyncpg.connect(connection_url)
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
    async def deactivate_wallet(wallet_id):
        conn = await asyncpg.connect(connection_url)
        wallet_id = int(wallet_id)
        await conn.execute(f"""
            update community_wallet
                set is_active = false,
                    deactivate_date = statement_timestamp()
            where wallet_id = {wallet_id}
        """)

    @staticmethod
    # пересмотреть БД (таблицы community_payment_goals и community_wallet)
    # может их пересмотреть и объединить в одну таблу
    # или разделить по-другому!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    async def get_wallet(community_id: str):
        conn = await asyncpg.connect(connection_url)
        community_id = int(community_id)

        wallets = await conn.fetch(f"""
            select wallet_name, wallet_id
            from community_wallet
            where community_id = {community_id}
        """)
        return wallets
