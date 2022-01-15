from models.goal import Goals
from aiohttp import web
import aiohttp_jinja2

class GoalView(web.View):
    @aiohttp_jinja2.template('goal.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        goals = await Goals.get_goals(user_id=self.session['user']['id'])
        return dict(goals=goals)