class Goals:
    @staticmethod
    async def get_goals(user_id: str, user_type: int, conn):
        if user_type == 0:
            table = 'users_information'
            column = 'user_id'
        if user_type == 1:
            table = 'communities'
            column = 'community_id'
        if user_type == 2:
            table = 'courses'
            column = 'course_id'
        goals = await conn.fetch(f"""
            select a.name, a.achievement_id
            from achievements a 
            right join (
                select unnest(achievements_desired_id) as desired_id 
                from {table} 
                where {column}={user_id}
                ) as u 
                on u.desired_id = a.achievement_id
                """)
        return goals