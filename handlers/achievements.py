import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.achievements import Achievements


class AchievementsView(web.View):

    @aiohttp_jinja2.template('achievements.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        achievements = await Achievements.get_user_achievements(user_id=self.session['user']['id'])
        return dict(achievements=achievements)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        session = await get_session(self)
        await Achievements.create_new_achievement(user_id=session['user']['id'], name=data['name'], description=data['description'])
        raise web.HTTPFound(location=self.app.router['achievements'].url_for())
