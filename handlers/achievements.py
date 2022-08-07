import aiohttp_jinja2
from aiohttp import web
import hashlib
import qrcode
from geopy import Nominatim
from aiohttp_session import get_session
from models.achievements import *
from aioipapi import IpApiClient
from geopy.distance import great_circle
from models.information import InfoGet
from models.user import UserGetInfo
from models.community import CommunityGetInfo
from models.course import CoursesGetInfo
from config.services_our_api import ServicesConfig
from config.common import BaseConfig
from models.api.tests import test_result
import json
from aiohttp.web import json_response


async def get_achievements(request):
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    async with pool.acquire() as conn:
        achievements_created = await AchievementsGetInfo.get_created_achievements(user_id=user_id, conn=conn)
        achievements_get = await AchievementsGetInfo.get_reached_achievements(user_id=user_id, conn=conn)
        achievements_sug = await AchievementsGetInfo.get_suggestion_achievements(user_id=user_id, conn=conn)
        spheres = await InfoGet.get_spheres(conn=conn)
        group = await AchievementsGenerateData.data_for_drop_downs_generate_achievements(conn=conn)
        groups = await AchievementsGenerateData.data_for_group_drop_down_generate_achievements(conn=conn)
        communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id, conn=conn)
        courses = await CoursesGetInfo.get_own_courses(user_id=user_id, conn=conn)
    return json_response({'my': achievements_created, 'suggestion': achievements_sug,
                          'get': achievements_get,
                          'create': {'group': group,
                                     'communities': communities, 'courses': courses, 'spheres': spheres,
                                     'groups': groups}
                          })


async def get_conditions_by_group(request):
    group_id = str(request).split('/')[-1][:-2]
    if group_id == 'null':
        agg = None
        services = None
        parameters = None
    else:
        pool = request.app['pool']
        async with pool.acquire() as conn:
            if group_id == '3':
                services = await InfoGet.get_services(conn=conn)
                agg, parameters = None, None
            else:
                services = None
                agg, parameters = await InfoGet.get_agg_par_by_group_id(group_id=group_id, conn=conn)
    return json_response({'services': services, 'agg': agg, 'parameters': parameters})


async def get_conditions_by_service(request):
    service_id = str(request).split('/')[-1][:-2]
    if service_id == 'null':
        agg = None
        parameters = None
    else:
        pool = request.app['pool']
        async with pool.acquire() as conn:
            agg, parameters = await InfoGet.get_agg_par_by_service_id(service_id=service_id, conn=conn)
    return json_response({'agg': agg, 'parameters': parameters})


async def get_conditions_by_agg_group(request):
    ids = str(request).split('/')[-1][:-2].split('_')
    if len(ids) == 2:
        group_id, agg_id = ids[0], ids[1]
        service_id = 'null'
    elif ids[0] != '3':
        group_id, agg_id = ids[0], ids[2]
        service_id = 'null'
    else:
        group_id, service_id, agg_id = ids[0], ids[1], ids[2]
    if agg_id == 'null' or group_id == 'null':
        parameters = None
    else:
        pool = request.app['pool']
        async with pool.acquire() as conn:
            if service_id != 'null':
                parameters = await InfoGet.get_par_by_agg_id_group_id_service(agg_id=agg_id, group_id=group_id,
                                                                              service_id=service_id, conn=conn)
            else:
                parameters = await InfoGet.get_par_by_agg_id_group_id(agg_id=agg_id, group_id=group_id, conn=conn)
    return json_response({'parameters': parameters})


async def get_subspheres_by_sphere(request):
    sphere_id = str(request).split('/')[-1][:-2]
    if sphere_id == 'null':
        subspheres = None
    else:
        pool = request.app['pool']
        async with pool.acquire() as conn:
            subspheres = await InfoGet.get_subsphere_id_by_sphere_id(sphere_id=sphere_id, conn=conn)
    return json_response({'subspheres': subspheres})


async def desire_achievement(request):
    pool = request.app['pool']
    data = await request.json()
    if data['user_type'] == 0:
        data['user_id'] = json.loads(request.cookies['user'])['user_id']
    async with pool.acquire() as conn:
        await AchievementsDesireApprove.desire_achievement(user_id=data['user_id'], user_type=data['user_type'],
                                                           achievement_desire_id=data['achievement_id'], conn=conn)
    return json_response({'value': 200})


async def drop_achievement(request):
    pool = request.app['pool']
    data = await request.json()
    if data['user_type'] == 0:
        data['user_id'] = json.loads(request.cookies['user'])['user_id']
    async with pool.acquire() as conn:
        could_drop = await AchievementsGetInfo.is_drop(achievement_id=data['achievement_id'], conn=conn)
        if could_drop:
            await AchievementsCreateDelete.delete_achievement(achievement_id=data['achievement_id'], conn=conn)
            achievements_created = await AchievementsGetInfo.get_created_achievements(user_id=data['user_id'],
                                                                                      conn=conn)
    return json_response({'value': achievements_created})


async def show_achievement(request):
    pool = request.app['pool']
    data = await request.json()
    if data['user_type'] == 0:
        data['user_id'] = json.loads(request.cookies['user'])['user_id']
    async with pool.acquire() as conn:
        await AchievementsGiveVerify.show_achievement(user_id=data['user_id'],
                                                      achievement_id=data['achievement_id'], conn=conn)
        achievements_get = await AchievementsGetInfo.get_reached_achievements(user_id=data['user_id'], conn=conn)
    return json_response({'value': achievements_get})


async def hide_achievement(request):
    pool = request.app['pool']
    data = await request.json()
    if data['user_type'] == 0:
        data['user_id'] = json.loads(request.cookies['user'])['user_id']
    async with pool.acquire() as conn:
        await AchievementsGiveVerify.hide_achievement(user_id=data['user_id'],
                                                      achievement_id=data['achievement_id'], conn=conn)
        achievements_get = await AchievementsGetInfo.get_reached_achievements(user_id=data['user_id'], conn=conn)
    return json_response({'value': achievements_get})


async def get_users_by_type(request):
    pool = request.app['pool']
    user_type = str(request).split('/')[-1][:-2]
    if user_type == 'null':
        users = None
    else:
        user_id = json.loads(request.cookies['user'])['user_id']
        async with pool.acquire() as conn:
            users = await UserGetInfo.get_community_course_by_type(user_id=user_id, user_type=user_type, conn=conn)
    return json_response({'users': users})


async def create_achievement(request):
    # todo: unique achievement name
    pool = request.app['pool']
    data = await request.json()
    print(data)
    if data['user_type'] == 0:
        data['user_id'] = json.loads(request.cookies['user'])['user_id']
    if data['dates'] != [None, None]:
        [data['from_date'], data['to_date']] = [i.split('T')[0] for i in data['dates']]
    elif data['dates'][0] is None and data['dates'][1] is not None:
        [data['from_date'], data['to_date']] = ['null', data['dates'][1].split('T')[0]]
    else:
        [data['from_date'], data['to_date']] = ['null', 'null']
    async with pool.acquire() as conn:
        data['select_group'], data['select_aggregation'] = \
            await InfoGet.get_conditions_by_parameter(data['select_parameter'], conn=conn)
        data['sphere'] = await InfoGet.get_sphere_id_by_subsphere_id(data['select_subsphere'], conn=conn)
    data['geo'] = 'null'
    data['achievement_qr'] = 'null'
    data['coords'] = ''
    if not data['test_url']:
        data['test_url'] = 'null'
        data['answers_url'] = 'null'
    if data['select_group'] == 1:

        token = hashlib.sha256(str(data['name'].replace(' ', '_').lower() +
                                   '_' + data['value'].replace(' ', '_').lower()).encode('utf8')).hexdigest()
        img = qrcode.make(f"http://localhost:3000/verify_achievement/{token}")
        img.save(f'{str(BaseConfig.STATIC_DIR) + "/QR/" + data["value"]}.png')
        data['achievement_qr'] = str(token)
    elif data['select_group'] == 2:
        if data['select_aggregation'] == 1:
            if data['coords'] != '' and data['value'] == '':
                location = data['coords'].replace(' ', '|').replace(',', '|').split('|')
                location = [float(i.replace('|', '')) for i in location if i != '']
                geolocator = Nominatim(user_agent="55")
                data['value'] = "_".join(
                    geolocator.reverse(f'{location[0]}, {location[1]}').address.replace(' ', '_').split(
                        ',')).replace('+', '')
            elif data['value'] != '' and data['coords'] == '':
                geolocator = Nominatim(user_agent="55")
                location = geolocator.geocode(data['value'])
                location = [location.latitude, location.longitude]
                print(location)
            else:
                location = data['coords'].replace(' ', '|').replace(',', '|').split('|')
                location = [float(i.replace('|', '')) for i in location if i != '']
            data['geo'] = f'CIRCLE(POINT({location[0]}, {location[1]}), 10)'
            print(data['geo'])
            data['achievement_qr'] = 'null'
    elif data['select_group'] == 6:
        data['test_url'] = data['test_web']
        data['answers_url'] = ''.join(data['answers_web'].split('/')[:3]) + '/export?format=csv'
        data['value'] = data['value'].replace(',', '.')
    elif data['select_group'] == 8:
        data['select_parameter'] = 'null'
        data['value'] = 'null'
    async with pool.acquire() as conn:
        achievement_id = await AchievementsCreateDelete.create_achievement(data=data, conn=conn)
    return json_response({'achievement': achievement_id})


async def undesire_achievement(request):
    pool = request.app['pool']
    user_id = json.loads(request.cookies['user'])['user_id']
    data = await request.json()
    user_type = data['user_type']
    achievement_id = data['achievement_id']
    async with pool.acquire() as conn:
        await AchievementsDesireApprove.undesire_achievement(user_id=user_id, user_type=user_type,
                                                             achievement_desire_id=achievement_id, conn=conn)
    return json_response({'value': {'desire': False}})


async def verify_achievement(request):
    pool = request.app['pool']
    data = await request.json()
    if str(request).split('/')[-1][:-2] == 'verify_achievement':
        achievement_id = data['achievement_id']
        qr_value = ''
    else:
        qr_value = data['qr_value']
        async with pool.acquire() as conn:
            achievement_id = await AchievementsGetInfo.get_achievement_by_token(token=qr_value, conn=conn)
    user_type = data['user_type']
    conditions_not_reached = None
    if user_type == 0:
        user_id = json.loads(request.cookies['user'])['user_id']
    else:
        user_id = data['user_id']
    reach = []
    async with pool.acquire() as conn:
        conditions = await AchievementsGetInfo.get_achievement_conditions(achievement_id=achievement_id,
                                                                          user_id=user_id, conn=conn)
    groups = [i for i in set([i['condition_group_id'] for i in conditions])]
    if 0 in groups:
        # todo: equality implementation
        user_conditions = [i for i in conditions if i['condition_group_id'] == 0]
        for i in user_conditions:
            result = False
            if i['aggregate_id'] == 0:
                async with pool.acquire() as conn:
                    value = await UserGetInfo.get_user_info_by_count(user_id=user_id,
                                                                     value=i['parameter_name'].replace(' ', '_'),
                                                                     conn=conn)
                if int(i['value']) <= value:
                    result = True
            elif i['aggregate_id'] == 1:
                async with pool.acquire() as conn:
                    value = await UserGetInfo.get_user_info_by_value(user_id=user_id,
                                                                     value=i['parameter_name'].replace(' ', '_'),
                                                                     conn=conn)
                if i['value'] == value:
                    result = True
            reach.append(result)
    if 1 in groups:
        async with pool.acquire() as conn:
            result = await AchievementsGiveVerify.qr_verify(value=qr_value, conn=conn)
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
            if distance / 1000 <= r:
                reach.append(True)
            else:
                reach.append(False)
            # if distance > 1000:
            # distance = distance/1000
            # val = 'km'
            # await AchievementsGiveVerify.location_verify(user_id=session['user']['id'], value=i['value'])
            # distance = distance
            # val = val
    if 3 in groups:
        service_conditions = [i for i in conditions if i['condition_group_id'] == 3]
        for i in service_conditions:
            i = dict(i)
            i['parameter_name'] = i['parameter_name'].replace('     ', '__r__').replace(' ', '_')
            service = ServicesConfig.service_classes[i['service_id']]
            functions = [j for j in ServicesConfig.service_functions.keys() if
                         service.__name__ in j and i['parameter_name'] in j][0]
            result = False
            if i['aggregate_id'] == 0:
                if i['equality'] == 1:
                    if ServicesConfig.service_functions[functions](i['services_username'],
                                                                   (i['parameter_name']))[i['parameter_name']] >= \
                            int(i['value']):
                        result = True
                elif i['equality'] == 0:
                    if ServicesConfig.service_functions[functions](i['services_username'],
                                                                   (i['parameter_name']))[i['parameter_name']] <= \
                            int(i['value']):
                        result = True
            elif i['aggregate_id'] == 1:
                if ServicesConfig.service_functions[functions](i['services_username'],
                                                               (i['parameter_name']))[i['parameter_name']] == \
                        i['value']:
                    result = True
            elif i['aggregate_id'] == 2:
                if ServicesConfig.service_functions[functions](i['services_username'],
                                                               (i['parameter_name']))[i['parameter_name']]:
                    result = True
            elif i['aggregate_id'] == 3:
                if i['equality'] == 1:
                    if ServicesConfig.service_functions[functions](i['services_username'],
                                                                   (i['parameter_name']))[i['parameter_name']] >= \
                            i['value']:
                        result = True
                elif i['equality'] == 0:
                    if ServicesConfig.service_functions[functions](i['services_username'],
                                                                   (i['parameter_name']))[i['parameter_name']] <= \
                            i['value']:
                        result = True
            reach.append(result)
    if 4 in groups:
        community_conditions = [i for i in conditions if i['condition_group_id'] == 4]
        for i in community_conditions:
            if i['aggregate_id'] == 0:
                async with pool.acquire() as conn:
                    value = await CommunityGetInfo.get_community_info_by_value(community_id=user_id,
                                                                               value=i['parameter_name'].replace(' ',
                                                                                                                 '_'),
                                                                               conn=conn)
                if int(i['value']) >= value:
                    reach.append(True)
                else:
                    reach.append(False)
    if 5 in groups:
        course_conditions = [i for i in conditions if i['condition_group_id'] == 5]
        for i in course_conditions:
            if i['aggregate_id'] == 0:
                async with pool.acquire() as conn:
                    value = await CoursesGetInfo.get_course_info_by_value(course_id=user_id,
                                                                          value=i['parameter_name'].replace(' ', '_'),
                                                                          conn=conn)
                if int(i['value']) >= value:
                    reach.append(True)
                else:
                    reach.append(False)
    if 6 in groups:
        test_conditions = [i for i in conditions if i['condition_group_id'] == 6]
        for i in test_conditions:
            async with pool.acquire() as conn:
                data = await AchievementsDesireApprove.get_data_for_test(user_id=user_id,
                                                                         condition_id=i['condition_id'], conn=conn)
            percentage = None
            if 'percentage' in i['parameter_name']:
                percentage = True
            result = test_result(email=data['email'], url=data['answers'], percentage=percentage)
            if result:
                if 'percentage' in i['parameter_name']:
                    # todo: не знаем сколько всего, не считаем percentage
                    pass
                if result >= float(i['value']):
                    reach.append(True)
                else:
                    reach.append(False)
            else:
                reach.append(False)
    if 7 in groups:
        approve_conditions = [i for i in conditions if i['condition_group_id'] == 7]
        for i in approve_conditions:
            async with pool.acquire() as conn:
                result = await AchievementsGiveVerify.approve_verify(user_id=user_id, parameter_id=i['parameter_id'],
                                                                     conn=conn)
            reach.append(result)
    if 8 in groups:
        no_verify_conditions = [i for i in conditions if i['condition_group_id'] == 8]
        for i in no_verify_conditions:
            reach.append(True)
    if False in reach:
        decline = True
        not_reached = [i for i, e in enumerate(reach) if e is False]
        conditions_not_reached = [dict(i) for i in conditions if conditions.index(i) in not_reached]
        async with pool.acquire() as conn:
            await AchievementsDesireApprove.desire_achievement(user_id=user_id, user_type=user_type,
                                                               achievement_desire_id=achievement_id, conn=conn)
    else:
        async with pool.acquire() as conn:
            await AchievementsGiveVerify.give_achievement_to_user(user_id=user_id, achievement_id=achievement_id,
                                                                  user_type=user_type, conn=conn)
            if await AchievementsDesireApprove.is_desire_achievement(user_id=user_id,
                                                                     achievement_id=achievement_id, conn=conn):
                await AchievementsDesireApprove.undesire_achievement(user_id=user_id, user_type=user_type,
                                                                     achievement_desire_id=achievement_id, conn=conn)
        decline = False
    return json_response({'value': {'desire': decline, 'conditions': conditions_not_reached,
                                    'is_reached': not decline, 'achievement_id': achievement_id}})


class AchievementsVerificationView(web.View):

    @aiohttp_jinja2.template('achievements_verify.html')
    async def post(self):

        session = await get_session(self)
        if str(self).split('/')[-1][:-2] == 'verify_achievement':
            achievement_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('achievement/')[
                                 -1][:-2]
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
        conditions = await AchievementsGetInfo.get_achievement_conditions(achievement_id=achievement_id,
                                                                          user_id=session['user']['id'])
        reach = []

        groups = [i for i in set([i['condition_group_id'] for i in conditions])]
        if 0 in groups:
            # todo: equality implementation
            user_conditions = [i for i in conditions if i['condition_group_id'] == 0]
            for i in user_conditions:
                result = False
                if i['aggregate_id'] == 0:
                    value = await UserGetInfo.get_user_info_by_count(user_id=user_id,
                                                                     value=i['parameter_name'].replace(' ', '_'))
                    if int(i['value']) <= value:
                        result = True
                elif i['aggregate_id'] == 1:
                    value = await UserGetInfo.get_user_info_by_value(user_id=user_id,
                                                                     value=i['parameter_name'].replace(' ', '_'))
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
                if distance / 1000 <= r:
                    reach.append(True)
                else:
                    reach.append(False)
                # if distance > 1000:
                # distance = distance/1000
                # val = 'km'
                # await AchievementsGiveVerify.location_verify(user_id=session['user']['id'], value=i['value'])
                # distance = distance
                # val = val
        if 3 in groups:
            service_conditions = [i for i in conditions if i['condition_group_id'] == 3]
            for i in service_conditions:
                i = dict(i)
                i['parameter_name'] = i['parameter_name'].replace('     ', '__r__').replace(' ', '_')
                service = ServicesConfig.service_classes[i['service_id']]
                functions = [j for j in ServicesConfig.service_functions.keys() if
                             service.__name__ in j and i['parameter_name'] in j][0]
                print(ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name'])))
                result = False
                if i['aggregate_id'] == 0:
                    if i['equality'] == 1:
                        if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[
                            i['parameter_name']] >= int(i['value']):
                            result = True
                    elif i['equality'] == 0:
                        if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[
                            i['parameter_name']] <= int(i['value']):
                            result = True
                elif i['aggregate_id'] == 1:
                    if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[
                        i['parameter_name']] == i['value']:
                        result = True
                elif i['aggregate_id'] == 2:
                    if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[
                        i['parameter_name']]:
                        result = True
                elif i['aggregate_id'] == 3:
                    if i['equality'] == 1:
                        if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[
                            i['parameter_name']] >= i['value']:
                            result = True
                    elif i['equality'] == 0:
                        if ServicesConfig.service_functions[functions](i['services_username'], (i['parameter_name']))[
                            i['parameter_name']] <= i['value']:
                            result = True
                reach.append(result)
        if 4 in groups:
            community_conditions = [i for i in conditions if i['condition_group_id'] == 4]
            for i in community_conditions:
                if i['aggregate_id'] == 0:
                    value = await CommunityGetInfo.get_community_info_by_value(community_id=user_id,
                                                                               value=i['parameter_name'].replace(' ',
                                                                                                                 '_'))
                    if int(i['value']) >= value:
                        reach.append(True)
                    else:
                        reach.append(False)
        if 5 in groups:
            course_conditions = [i for i in conditions if i['condition_group_id'] == 5]
            for i in course_conditions:
                if i['aggregate_id'] == 0:
                    value = await CoursesGetInfo.get_course_info_by_value(course_id=user_id,
                                                                          value=i['parameter_name'].replace(' ', '_'))
                    if int(i['value']) >= value:
                        reach.append(True)
                    else:
                        reach.append(False)
        if 6 in groups:
            test_conditions = [i for i in conditions if i['condition_group_id'] == 6]
            for i in test_conditions:
                data = await AchievementsDesireApprove.get_data_for_test(user_id=user_id,
                                                                         condition_id=i['condition_id'])
                percentage = None
                if 'percentage' in i['parameter_name']:
                    percentage = True
                result = test_result(email=data['email'], url=data['answers'], percentage=percentage)
                if result:
                    if 'percentage' in i['parameter_name']:
                        # todo: не знаем сколько всего, не считаем percentage
                        pass
                    if result >= float(i['value']):
                        reach.append(True)
                    else:
                        reach.append(False)
                else:
                    reach.append(False)
        if 7 in groups:
            approve_conditions = [i for i in conditions if i['condition_group_id'] == 7]
            for i in approve_conditions:
                result = await AchievementsGiveVerify.approve_verify(user_id=user_id, parameter_id=i['parameter_id'])
                reach.append(result)
        if 8 in groups:
            no_verify_conditions = [i for i in conditions if i['condition_group_id'] == 8]
            for i in no_verify_conditions:
                reach.append(True)
        conditions_not_reached = []
        if False in reach:
            decline = True
            not_reached = [i for i, e in enumerate(reach) if e is False]
            conditions_not_reached = [i for i in conditions if conditions.index(i) in not_reached]
        else:
            await AchievementsGiveVerify.give_achievement_to_user(user_id=user_id, achievement_id=achievement_id,
                                                                  user_type=user_type)
            decline = False
        achievement = await AchievementsGetInfo.get_achievement_info(achievement_id)
        return dict(achievement=achievement, decline=decline, conditions_not_reached=conditions_not_reached)


async def get_achievement_info(request):
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    async with pool.acquire() as conn:
        communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id, conn=conn)
        courses = await CoursesGetInfo.get_own_courses(user_id=user_id, conn=conn)
        achievement_id = str(request).split('/')[-1][:-2]
        achievement = await AchievementsGetInfo.get_achievement_info(achievement_id=achievement_id, conn=conn)
        is_owner = await AchievementsGetInfo.is_achievement_owner(user_id=user_id, achievement_id=achievement_id,
                                                                  conn=conn)
        desire = await AchievementsDesireApprove.is_desire_achievement(user_id=user_id,
                                                                       achievement_id=achievement_id, conn=conn)
        is_reached = await AchievementsGetInfo.is_reach_achievement(user_id=user_id, achievement_id=achievement_id,
                                                                    conn=conn)
        return json_response({'achievement': achievement, 'desire': desire, 'is_owner': is_owner, 'communities':
                             communities, 'courses': courses, 'is_reached': is_reached})


class AchievementInfoView(web.View):
#     @aiohttp_jinja2.template('achievement_info.html')
#     async def get(self):
#
#         session = await get_session(self)
#         user_id = session['user']['id']
#         communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id)
#         courses = await CoursesGetInfo.get_own_courses(user_id=user_id)
#
#         location = str(self).split('/achievement/')[-1][:-2]
#         achievement = await AchievementsGetInfo.get_achievement_info(achievement_id=location)
#         if achievement['achi_condition_group_id'] == 7:
#             desire = await AchievementsDesireApprove.is_desire(user_id=user_id, achievement_desire_id=location)
#         else:
#             desire = False
#         return dict(achievement=achievement, desire=desire, communities=communities, courses=courses)

    @aiohttp_jinja2.template('achievements_verify.html')
    async def post(self):

        data = await self.post()
        session = await get_session(self)
        achievement = await AchievementsGetInfo.get_achievement_by_condition_id(condition_id=data['achi'])
        if achievement[0]['value'] == data['message']:
            result = await AchievementsGiveVerify.give_achievement_to_user(achievement[0]['achievement_id'],
                                                                           session['user']['id'])
            if result:
                return dict(decline=True, achievement=achievement)
            else:
                return dict(achievement=achievement)
        else:
            return dict(decline=True, achievement=achievement)


class AchievementDesireView(web.View):
    async def post(self):

        data = await self.post()
        session = await get_session(self)
        url = str(self).split('/')[-1][:-2]
        if url != 'desire':
            await AchievementsDesireApprove.approve_achievement(user_active_id=session['user']['id'], user_passive_id=
            str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('user/')[-1][:-2],
                                                                achievement_id=data['achi_id'])
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
            achievement_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('achievement/')[
                                 -1][:-2]
            await AchievementsDesireApprove.desire_achievement(user_id=user_id, user_type=user_type,
                                                               achievement_desire_id=achievement_id)
            return web.HTTPFound(location=f"achievement/{data['achi_id']}")
