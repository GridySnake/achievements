import aiohttp_jinja2
from aiohttp import web
import json
import hashlib
import qrcode
from geopy import Nominatim
from aiohttp_session import get_session
from models.achievements import *
from aioipapi import IpApiClient
from geopy.distance import great_circle
from models.information import InfoGet
from models.user import UserGetInfo
from models.api.chess_com import Chesscom
from models.community import CommunityGetInfo
from models.course import CoursesGetInfo
from config.services_our_api import ServicesConfig
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
        # await AchievementsGiveVerify.desired_to_reached_achievement(user_id=user_id)
        achievements_created = await AchievementsGetInfo.get_created_achievements(user_id=user_id)
        achievements_get = await AchievementsGetInfo.get_reached_achievements(user_id=user_id)
        achievements_sug = await AchievementsGetInfo.get_suggestion_achievements(user_id=user_id)
        # spheres = await InfoGet.get_spheres()
        subspheres = await InfoGet.get_subspheres()
        group = await AchievementsGenerateData.data_for_drop_downs_generate_achievements()
        # values = [dict(record) if record['service_id'] is not None else {key: dict(record).get(key) for key in dict(record).keys() if key not in ['service_id', 'service_name']} for record in dropdown_create]
        # dropdown_create_json = json.dumps(values).replace("</", "<\\/")
        groups = await AchievementsGenerateData.data_for_group_drop_down_generate_achievements()
        services = await InfoGet.get_services()
        communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id)
        courses = await CoursesGetInfo.get_own_courses(user_id=user_id)
        return dict(achievements_my=achievements_created, achievements_sug=achievements_sug, achievements_get=achievements_get, services=services, group=group, communities=communities, courses=courses, subspheres=subspheres, groups=groups)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        data = await self.post()
        data = dict(data)
        # todo: unique achievement name
        session = await get_session(self)
        user_id = session['user']['id']
        user_type = 0
        if 'achi_as_community' in data.keys():
            user_type = 1
            user_id = data['achi_community']
        elif 'achi_as_course' in data.keys():
            user_type = 2
            user_id = data['achi_course']
        data['geo'] = 'null'
        data['achievement_qr'] = 'null'
        if data['select_group'] == '1':
            token = hashlib.sha256(data['name'].replace(' ', '_').lower().encode('utf8')).hexdigest()
            img = qrcode.make(f"http://127.0.0.1:8080/verify_achievement/{token}")
            img.save(f'{str(BaseConfig.STATIC_DIR) + "/QR/" + str(token)}.png')
            data['achievement_qr'] = str(token)
        elif data['select_group'] == '2':
            if data['select_aggregation'] == '1':
                if data['coords'] != '' and data['value'] == '':
                    location = data['coords'].replace(' ', '|').replace(',', '|').split('|')
                    location = [float(i.replace('|', '')) for i in location if i != '']
                    geolocator = Nominatim(user_agent="55")
                    data['value'] = "_".join(geolocator.reverse(f'{location[0]}, {location[1]}').address.replace(' ', '_').split(',')).replace('+', '')
                elif data['value'] != '' and data['coords'] == '':
                    geolocator = Nominatim(user_agent="55")
                    location = geolocator.geocode(data['value'])
                    location = [location.latitude, location.longitude]
                else:
                    location = data['coords'].replace(' ', '|').replace(',', '|').split('|')
                    location = [float(i.replace('|', '')) for i in location if i != '']
                data['geo'] = f'CIRCLE(POINT({location[0]}, {location[1]}), 10)'
                data['achievement_qr'] = 'null'
        data['sphere'] = await InfoGet.get_sphere_id_by_subsphere_id(data['select_subsphere'])
        await AchievementsCreate.create_achievement(user_id=user_id, user_type=user_type, data=data)
        return web.HTTPFound(location=self.app.router['achievements'].url_for())


class AchievementsVerificationView(web.View):

    @aiohttp_jinja2.template('achievements_verify.html')
    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        session = await get_session(self)
        if str(self).split('/')[-1][:-2] == 'verify_achievement':
            achievement_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('achievement/')[-1][:-2]
        else:
            qr_value = str(self).split('/')[-1][:-2]
            achievement_id = await AchievementsGetInfo.get_achievement_by_condition_value(value=qr_value)
            if not achievement_id:
                return dict(decline=True)

        data = await self.post()
        data = dict(data)
        if 'verify_achi_community' in data.keys():
            user_type = 1
            user_id = data['verify_achi_community']
        elif 'verify_achi_course' in data.keys():
            user_type = 2
            user_id = data['verify_achi_course']
        else:
            user_type = 0
            user_id = session['user']['id']
        conditions = await AchievementsGetInfo.get_achievement_conditions(achievement_id=achievement_id, user_id=session['user']['id'])
        reach = []

        groups = [i for i in set([i['condition_group_id'] for i in conditions])]
        print(conditions)
        if 0 in groups:
            # todo: equality implementation
            user_conditions = [i for i in conditions if i['condition_group_id'] == 0]
            for i in user_conditions:
                result = False
                if i['aggregate_id'] == 0:
                    value = await UserGetInfo.get_user_info_by_count(user_id=user_id, value=i['parameter_name'].replace(' ', '_'))
                    if int(i['value']) <= value:
                        result = True
                elif i['aggregate_id'] == 1:
                    value = await UserGetInfo.get_user_info_by_value(user_id=user_id, value=i['parameter_name'].replace(' ', '_'))
                    if i['value'] == value:
                        result = True
                reach.append(result)
                # result = await AchievementsGiveVerify.user_info_achievements_verify(achievement_id=achievement_id, value=str(value))

        if 1 in groups:
            result = await AchievementsGiveVerify.qr_verify(user_id=session['user']['id'], value=qr_value)
            reach.append(result)
        if 2 in groups:
            async with IpApiClient() as client:
                loc = await client.location()
            coord = (loc['lat'], loc['lon'])
            geo_conditions = [i for i in conditions if i['condition_group_id'] == 2]
            for i in geo_conditions:
                coords_achi = i['geo']
                r = coords_achi[-1]
                distance = great_circle((coord[0], coord[1]), (coords_achi[0][0], coords_achi[0][1])).meters
                # val = 'm'
                if distance/1000 <= r:
                    reach.append(True)
                else:
                    reach.append(False)
                # if distance > 1000:
                    # distance = distance/1000
                    # val = 'km'
                    #await AchievementsGiveVerify.location_verify(user_id=session['user']['id'], value=i['value'])
                # distance = distance
                # val = val
        if 3 in groups:
            service_conditions = [i for i in conditions if i['condition_group_id'] == 3]
            for i in service_conditions:
                i = dict(i)
                i['parameter_name'] = i['parameter_name'].replace('     ', '__r__').replace(' ', '_')
                service = ServicesConfig.service_classes[i['service_id']]
                functions = [j for j in ServicesConfig.service_functions.keys() if service.__name__ in j and i['parameter_name'] in j][0]
                print(ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name'])))
                result = False
                if i['aggregate_id'] == 0:
                    if i['equality'] == 1:
                        if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[i['parameter_name']] >= int(i['value']):
                            result = True
                    elif i['equality'] == 0:
                        if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[i['parameter_name']] <= int(i['value']):
                            result = True
                elif i['aggregate_id'] == 1:
                    if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[i['parameter_name']] == i['value']:
                        result = True
                elif i['aggregate_id'] == 2:
                    if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[i['parameter_name']]:
                        result = True
                elif i['aggregate_id'] == 3:
                    if i['equality'] == 1:
                        if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[i['parameter_name']] >= i['value']:
                            result = True
                    elif i['equality'] == 0:
                        if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[i['parameter_name']] <= i['value']:
                            result = True
                reach.append(result)
        if 4 in groups:
            community_conditions = [i for i in conditions if i['condition_group_id'] == 4]
            for i in community_conditions:
                if i['aggregate_id'] == 0:
                    value = await CommunityGetInfo.get_community_info_by_value(community_id=user_id, value=i['parameter_name'].replace(' ', '_'))
                    if int(i['value']) >= value:
                        reach.append(True)
                    else:
                        reach.append(False)
        if 5 in groups:
            course_conditions = [i for i in conditions if i['condition_group_id'] == 5]
            for i in course_conditions:
                if i['aggregate_id'] == 0:
                    value = await CoursesGetInfo.get_course_info_by_value(course_id=user_id, value=i['parameter_name'].replace(' ', '_'))
                    if int(i['value']) >= value:
                        reach.append(True)
                    else:
                        reach.append(False)
        if 7 in groups:
            approve_conditions = [i for i in conditions if i['condition_group_id'] == 7]
            for i in approve_conditions:
                result = await AchievementsGiveVerify.approve_verify(user_id=user_id, parameter_id=i['parameter_id'])
                reach.append(result)
        conditions_not_reached = []
        if False in reach:
            decline = True
            not_reached = [i for i, e in enumerate(reach) if e is False]
            conditions_not_reached = [i for i in conditions if conditions.index(i) in not_reached]
        else:
            await AchievementsGiveVerify.give_achievement_to_user(user_id=user_id, achievement_id=achievement_id, user_type=user_type)
            decline = False
        achievement = await AchievementsGetInfo.get_achievement_info(achievement_id)
        return dict(achievement=achievement, decline=decline, conditions_not_reached=conditions_not_reached)


class AchievementInfoView(web.View):
    @aiohttp_jinja2.template('achievement_info.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        session = await get_session(self)
        user_id = session['user']['id']
        communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id)
        courses = await CoursesGetInfo.get_own_courses(user_id=user_id)

        location = str(self).split('/achievement/')[-1][:-2]
        achievement = await AchievementsGetInfo.get_achievement_info(achievement_id=location)
        print(achievement)
        if achievement['achi_condition_group_id'] == 7:
            desire = await AchievementsDesireApprove.is_desire(user_id=user_id, achievement_desire_id=location)
        else:
            desire = False
        return dict(achievement=achievement, desire=desire, communities=communities, courses=courses)

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
            await AchievementsDesireApprove.approve_achievement(user_active_id=session['user']['id'], user_passive_id=str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('user/')[-1][:-2], achievement_id=data['achi_id'])
            return web.HTTPFound(location=f"/{data['user_passive_id']}")
        else:
            user_id = session['user']['id']
            user_type = 0
            data = dict(data)
            if 'desire_achi_as_community' in data.keys():
                user_type = 1
                user_id = data['desire_achi_community']
            elif 'desire_achi_as_course' in data.keys():
                user_type = 2
                user_id = data['desire_achi_course']
            achievement_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('achievement/')[-1][:-2]
            await AchievementsDesireApprove.desire_achievement(user_id=user_id, user_type=user_type, achievement_desire_id=achievement_id)
            return web.HTTPFound(location=f"achievement/{data['achi_id']}")
