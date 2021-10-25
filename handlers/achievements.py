import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.achievements import Achievements
from aioipapi import IpApiClient
from geopy.distance import great_circle


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
        types = location.split('/')[0]
        if types == 'qr':
            result = await Achievements.qr_verify(user_id=session['user']['id'], value=location.split('/')[-1])
            if result:
                return web.HTTPForbidden()
            else:
                achievement = await Achievements.get_achievement_by_condition_value(value=location.split('/')[-1])
                return dict(achievement=achievement)
        elif types == 'location':
            async with IpApiClient() as client:
                loc = await client.location()
            coord = (loc['lat'], loc['lon'])
            coord_achi = await Achievements.get_achievement_by_condition_id(condition_id=location.split('/')[-1])
            r = coord_achi[0]['geo'][-1]
            distance = great_circle((coord[0], coord[1]), (coord_achi[0]['geo'][0][0], coord_achi[0]['geo'][0][1])).meters
            val = 'm'
            if distance/1000 <= r:
                result = True
            else:
                result = False
            if distance > 1000:
                distance = distance/1000
                val = 'km'
            if result:
                await Achievements.location_verify(user_id=session['user']['id'], value=location.split('/')[-1])
                return dict(achievement=coord_achi)
            else:
                return dict(decline=True, achievement=coord_achi, distance=distance, val=val)


class AchievementInfoView(web.View):
    @aiohttp_jinja2.template('achievement_info.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        location = str(self).split('/achievement/')[-1][:-2]
        achievement = await Achievements.get_achievement_info(achievement_id=location)
        return dict(achievement=achievement)
