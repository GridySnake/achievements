import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.achievements import Achievements


class AchievementsView(web.View):

    @aiohttp_jinja2.template('achievements.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()
        await Achievements.update_user_info_achievements(user_id=self.session['user']['id'])
        achievements_my = await Achievements.get_created_achievements(user_id=self.session['user']['id'])
        achievements_get = await Achievements.get_reached_achievements(user_id=self.session['user']['id'])
        achievements_sug = await Achievements.get_suggestion_achievements(user_id=self.session['user']['id'])
        return dict(achievements_my=achievements_my, achievements_sug=achievements_sug, achievements_get=achievements_get)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        session = await get_session(self)
        print(data)
        await Achievements.create_new_achievement(user_id=session['user']['id'], data=data)
        raise web.HTTPFound(location=self.app.router['achievements'].url_for())
