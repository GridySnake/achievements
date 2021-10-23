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
        achievements_created = await Achievements.get_created_achievements(user_id=self.session['user']['id'])
        achievements_get = await Achievements.get_reached_achievements(user_id=self.session['user']['id'])
        achievements_sug = await Achievements.get_suggestion_achievements(user_id=self.session['user']['id'])
        return dict(achievements_my=achievements_created, achievements_sug=achievements_sug, achievements_get=achievements_get)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        session = await get_session(self)
        await Achievements.create_new_achievement(user_id=session['user']['id'], data=data)
        raise web.HTTPFound(location=self.app.router['achievements'].url_for())


class AchievementsVerificationView(web.View):

    @aiohttp_jinja2.template('achievements_verify.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        session = await get_session(self)
        location = str(self).split('/verify_achievement/')[-1][:-2]
        result = await Achievements.qr_verify(user_id=session['user']['id'], value=location)
        if result:
            return web.HTTPForbidden()
        else:
            achievement = await Achievements.get_achievement_by_condition_value(value=location)
            print(achievement[0]['name'])
            return dict(achievement=achievement)
