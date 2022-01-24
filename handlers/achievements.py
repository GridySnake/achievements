import aiohttp_jinja2
from aiohttp import web
import json
from aiohttp_session import get_session
from models.achievements import *
from aioipapi import IpApiClient
from geopy.distance import great_circle
from models.information import InfoGet
from models.user import UserGetInfo
from models.api.chess_com import Chesscom
from models.community import CommunityGetInfo
from models.course import CoursesGetInfo
from models.api.twitch_tv import Twitch
from models.api.youtube import Youtube
from models.api.instagram import Instagram
from models.api.steam_games import Steam
from models.api.stepik import Stepik
from models.api.fitnesspal import Fitnesspal


class AchievementsView(web.View):

    @aiohttp_jinja2.template('achievements.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        user_id = self.session['user']['id']
        #await Achievements.update_user_info_achievements(user_id=user_id)
        await AchievementsGiveVerify.desired_to_reached_achievement(user_id=user_id)
        achievements_created = await AchievementsGetInfo.get_created_achievements(user_id=user_id)
        achievements_get = await AchievementsGetInfo.get_reached_achievements(user_id=user_id)
        achievements_sug = await AchievementsGetInfo.get_suggestion_achievements(user_id=user_id)
        spheres = await InfoGet.get_spheres()
        subspheres = await InfoGet.get_subspheres()
        dropdown_create = await AchievementsGenerateData.data_for_drop_downs_generate_achievements()
        values = [dict(record) if record['service_id'] is not None else {key: dict(record).get(key) for key in dict(record).keys() if key not in ['service_id', 'service_name']} for record in dropdown_create]
        dropdown_create_json = json.dumps(values).replace("</", "<\\/")
        group = await AchievementsGenerateData.data_for_group_drop_down_generate_achievements()
        services = await InfoGet.get_services()
        communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id)
        courses = await CoursesGetInfo.get_own_courses(user_id=user_id)
        return dict(achievements_my=achievements_created, achievements_sug=achievements_sug, achievements_get=achievements_get, services=services, dropdown=dropdown_create, dropdown_json=dropdown_create_json, group=group, communities=communities, courses=courses, subspheres=subspheres)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        data = await self.post()
        session = await get_session(self)
        user_id = session['user']['id']
        user_type = 0
        if 'achi_as_community' in data.keys():
            user_type = 1
            user_id = data['achi_community']
        elif 'achi_as_course' in data.keys():
            user_type = 2
            user_id = data['achi_course']
        if data['select_group'] == '1':
            token = hashlib.sha256(data['name'].replace(' ', '_').lower().encode('utf8')).hexdigest()
            img = qrcode.make(f"http://127.0.0.1:8080/verify_achievement/{token}")
            img.save(f'{str(BaseConfig.STATIC_DIR) + "/QR/" + str(token)}.png')
            data = dict(data)
            data['value'] = token
        elif data['select_group'] == '2':
            geolocator = Nominatim(user_agent="55")
            location = geolocator.geocode(data['value'])
            data = dict(data)
            data['lat'] = location.latitude
            data['lon'] = location.longitude
            data['radius'] = 10
        elif data['select_group'] == '8':
            data = dict(data)
            data['select_parameter'] = None
        data['sphere'] = await InfoGet.get_sphere_id_by_subsphere_id(data['select_subsphere'])
        await AchievementsCreate.create_achievement(user_id=user_id, user_type=user_type, data=data)
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
            result = await AchievementsGiveVerify.qr_verify(user_id=session['user']['id'], value=location.split('/')[-1])
            achievement = await AchievementsGetInfo.get_achievement_by_condition_value(value=location.split('/')[-1])
            if result:
                return dict(decline=True, achievement=achievement)
            else:
                return dict(achievement=achievement)
        elif types == 'location':
            async with IpApiClient() as client:
                loc = await client.location()
            coord = (loc['lat'], loc['lon'])
            coord_achi = await AchievementsGetInfo.get_achievement_by_condition_id(condition_id=location.split('/')[-1])
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
                await AchievementsGiveVerify.location_verify(user_id=session['user']['id'], value=location.split('/')[-1])
                return dict(achievement=coord_achi)
            else:
                return dict(decline=True, achievement=coord_achi, distance=distance, val=val)
        elif types == 'service':
            parameters = location[location.find('/')+1:].split('-')
            is_connected = await UserGetInfo.check_connect(session['user']['id'], parameters[0])
            if is_connected:
                username = await UserGetInfo.get_user_name_by_service(session['user']['id'], parameters[0])
                username = username[0][0]
                if parameters[1] == 'profile':
                    profile = Chesscom.get_player_profile(username)[parameters[2]]
                    if parameters[2] == 'country':
                        profile = profile.split('/')[-1]
                        profile = await InfoGet.get_country_by_iso(profile)
                        profile = profile[0][0]
                    achievement = await AchievementsGetInfo.get_achievement_by_condition_parameter(location[location.find('/')+1:])
                    if profile == achievement[0]['value']:
                        await AchievementsGiveVerify.chess_verify(user_id=session['user']['id'], achievement_id=str(achievement[0]['achievement_id']))
                        return dict(achievement=achievement)
                    else:
                        return dict(decline=True, achievement=achievement)

                elif 'profile_stats' in parameters[1]:
                    chess = Chesscom.get_player_stats(username)[parameters[1].replace('profile_stats_', '')][parameters[2]]['rating']
                    achievement = await AchievementsGetInfo.get_achievement_by_condition_parameter(location[location.find('/') + 1:])
                    result = False
                    if parameters[3] == 'more':
                        if chess > int(achievement[0]['value']):
                            result = True
                    if parameters[3] == 'less':
                        if chess < int(achievement[0]['value']):
                            result = True
                    if parameters[3] == 'equal':
                        if chess == int(achievement[0]['value']):
                            result = True
                    if result:
                        await AchievementsGiveVerify.chess_verify(user_id=session['user']['id'], achievement_id=str(achievement[0]['achievement_id']))
                        return dict(achievement=achievement)
                    else:
                        return dict(decline=True, achievement=achievement)

                elif parameters[1] == 'title':
                    achievement = await AchievementsGetInfo.get_achievement_by_condition_parameter(location[location.find('/') + 1:])
                    title = Chesscom.get_titled_players(achievement[0]['value'])['players']
                    if username in title:
                        await AchievementsGiveVerify.chess_verify(user_id=session['user']['id'], achievement_id=str(achievement[0]['achievement_id']))
                        return dict(achievement=achievement)
                    else:
                        return dict(decline=True, achievement=achievement)

                elif parameters[1] == 'leaderboard_daily':
                    title = Chesscom.get_leaderboards()['daily']
                    achievement = await AchievementsGetInfo.get_achievement_by_condition_parameter(location[location.find('/') + 1:])
                    if username in [i['username'] for i in title]:
                        await AchievementsGiveVerify.chess_verify(user_id=session['user']['id'], achievement_id=str(achievement[0]['achievement_id']))
                        return dict(achievement=achievement)
                    else:
                        return dict(decline=True, achievement=achievement)


class AchievementInfoView(web.View):
    @aiohttp_jinja2.template('achievement_info.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        session = await get_session(self)
        location = str(self).split('/achievement/')[-1][:-2]
        achievement = await AchievementsGetInfo.get_achievement_info(achievement_id=location)
        if achievement['parameter'] == 'user_approve':
            desire = await AchievementsDesireApprove.is_desire(user_id=session['user']['id'], achievement_desire_id=location)
        else:
            desire = False
        return dict(achievement=achievement, desire=desire)

    @aiohttp_jinja2.template('achievements_verify.html')
    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        data = await self.post()
        session = await get_session(self)
        achievement = await AchievementsGetInfo.get_achievement_by_condition_id(condition_id=data['achi'])
        if achievement[0]['value'] == data['message']:
            result = await AchievementsGiveVerify.give_achievement_to_user(achievement[0]['achievement_id'], session['user']['id'])
            if result:
                return dict(decline=True, achievement=achievement)
            else:
                return dict(achievement=achievement)
        else:
            return dict(decline=True, achievement=achievement)


class AchievementDesireView(web.View):
    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        data = await self.post()
        session = await get_session(self)
        url = str(self).split('/')[-1][:-2]
        if url != 'desire':
            await AchievementsDesireApprove.approve_achievement(user_active_id=session['user']['id'], user_passive_id=str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('8080/')[1][:-2], achievement_id=data['achi_id'])
            return web.HTTPFound(location=f"/{data['user_passive_id']}")
        else:
            await AchievementsDesireApprove.desire_achievement(user_id=session['user']['id'], achievement_desire_id=data['achi_id'])
            return web.HTTPFound(location=f"achievement/{data['achi_id']}")
