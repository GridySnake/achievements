from models.goal import Goals
from aiohttp import web
import aiohttp_jinja2


class GoalView(web.View):
    @aiohttp_jinja2.template('goal.html')
    async def get(self):
        goals = await Goals.get_goals(user_id=json.loads(request.cookies['user'])['user_id'])
        return dict(goals=goals)
