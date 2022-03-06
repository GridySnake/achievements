import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.conditions import ConditionsGetInfo, ConditionsInsertCheck
from models.api.tests import test_result
from config.common import BaseConfig
from models.course import CoursesGetInfo
from models.community import CommunityGetInfo
import json


class ApproveConditionsView:

    @aiohttp_jinja2.template('cover_letters_interviews.html')
    async def get(self):
        session = await get_session(self)
        user_id = str(session['user']['id'])
        owner = {'user': 0, 'community': 1,
                 'course': 2}
        for i in owner.keys():
            if i in str(self):
                owner_type = owner[i]
                owner_id = str(self).split(f'{i}/')[-1].split('/')[0]
                break
        owner = False
        if owner_type == 0 and user_id == owner_id:
            owner = True
        elif owner_type == 1:
            owner = await CommunityGetInfo.is_owner(user_id=user_id, community_id=owner_id)
        elif owner_type == 2:
            owner = await CoursesGetInfo.is_owner(course_id=owner_id, user_id=user_id)
        if not owner:
            return web.HTTPForbidden()
        else:
            cover_letters = await ConditionsGetInfo.get_cover_letters(receiver_id=owner_id, receiver_type=owner_type)
            interviews_request = await ConditionsGetInfo.get_interviews_requests(sender_id=owner_id,
                                                                                 sender_type=owner_type)
            interviews_future = await ConditionsGetInfo.get_interviews_future(sender_id=owner_id,
                                                                              sender_type=owner_type)
            return dict(cover_letters=cover_letters, interviews_request=interviews_request,
                        interviews_future=interviews_future)

    async def post(request):
        user_id = ''
        data = await request.json()
        data = dict(data)
        owner = {'user': ['users_information', 'user_id', 0], 'community': ['communities', 'community_id', 1],
                 'course': ['courses', 'course_id', 2]}
        for i in owner.keys():
            if i in str(self.__dict__['_message']).split('Referer')[-1].split(',')[1]:
                owner_type = owner[i]
                if 'cover_letter_interview' in str(self.__dict__['_message']).split('Referer')[-1].split(',')[1]:
                    owner_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/')[-2]
                else:
                    owner_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split(f'{i}/')[-1][:-2]
                break
        if 'update_interview' in str(self):
            location = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split(
                'http://localhost:8080/')[-1][:-2]
            data['datetime'] = ' '.join(data['datetime'].split('T')) + ':00.123456 +00:00'
            await ConditionsInsertCheck.update_interview_info(sender_id=owner_id, sender_type=owner_type, data=data)
        elif '_cl' in str(self) or '_int' in str(self):
            location = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split(
                'http://localhost:8080/')[-1][:-2]
            if 'accept' in str(self):
                status = 1
            else:
                status = -1
            if '_cl' in str(self):
                await ConditionsInsertCheck.accept_decline_cover_letter(user_id=user_id, receiver_id=owner_id,
                                                                        receiver_type=owner_type, status=status)
            elif '_int' in str(self):
                await ConditionsInsertCheck.accept_decline_interview(user_id=user_id, sender_id=owner_id,
                                                                     sender_type=owner_type, status=status)
        else:
            conditions = await ConditionsGetInfo.get_conditions(user_id=user_id, owner_id=owner_id, owner_type=owner_type)
            if conditions:
                result = []
                for i in conditions:
                    if 'reach' in i['condition_name'] and 'in sphere' not in i['condition_name']:
                        if 'created' in i['condition_name']:
                            parameter = 'create_' + i['condition_name'].split(' ')[0]
                        elif 'completed' in i['condition_name']:
                            parameter = 'completed_' + i['condition_name'].split(' ')[0]
                        else:
                            parameter = i['condition_name'].replace('reach ', '')
                        result.append(await ConditionsGetInfo.get_condition_user_statistics(user_id=user_id,
                                                                                            # owner_type=owner_type,
                                                                                            condition_name=parameter,
                                                                                            condition_value=
                                                                                            i['condition_value']
                                                                                            ))
                    elif 'in sphere' in i['condition_name']:
                        pass
                    elif 'only' in i['condition_name']:
                        result.append(await ConditionsGetInfo.is_follower(user_active_id=user_id, user_passive_id=owner_id,
                                                                          parameter=i['condition_name'].replace(' only', '')
                                                                          ))
                    elif 'test' in i['condition_name']:
                        data = await ConditionsGetInfo.get_data_for_condition_test(user_id=user_id,
                                                                                   condition_id=i['condition_id'])
                        percentage = None
                        if '%' in i['condition_value']:
                            # todo: не знаем сколько всего, не считаем percentage
                            pass
                        result = test_result(email=data['email'], url=data['answers'], percentage=percentage)
                        if result:
                            if result >= float(i['condition_value']):
                                result.append(True)
                            else:
                                result.append(False)
                    elif 'task' in i['condition_name']:
                        if f'{i["task"]}_condition_value' in data.keys():
                            if data[f'{i["task"]}_condition_value'] == i['condition_value']:
                                result.append(True)
                            else:
                                result.append(False)
                        else:
                            result.append(False)
                    elif 'cover letter' == i['condition_name']:
                        data_new = {}
                        if data['cover_letter'] != '':
                            data_new['letter_text'] = data['cover_letter']
                        else:
                            data_new['letter_text'] = 'null'
                        if data['cover_letter_file'] != bytearray(b''):
                            cl = data['cover_letter_file']
                            with open(BaseConfig.STATIC_DIR +
                                                   f"/cover_letter/{owner_type[1].replace('_id', '')}_{owner_id}_{user_id}_"
                                                   + cl.filename, 'wb') as f:
                                contents = cl.file.read()
                                f.write(contents)
                            data_new['letter_href'] = \
                                f"{owner_type[1].replace('_id', '')}_{owner_id}_{user_id}_{cl.filename}"
                        else:
                            data_new['letter_href'] = 'null'
                        if data_new['letter_href'] != 'null' or data_new['letter_text'] != 'null':
                            await ConditionsInsertCheck.send_cover_letter(user_id=user_id, owner_id=owner_id,
                                                                          owner_type=owner_type, data=data_new,
                                                                          condition_id=i['condition_id'])
                        else:
                            print('no data')
                    elif 'interview' == i['condition_name']:
                        send = await ConditionsGetInfo.is_send(user_id=user_id, sender_id=owner_id,
                                                               sender_type=owner_type)
                        if len(conditions) - 1 == len(result) and (not result or False not in result) and not send:
                            await ConditionsInsertCheck.request_interview(user_id=user_id, owner_id=owner_id,
                                                                          owner_type=owner_type,
                                                                          condition_id=i['condition_id'])
                conditions = [i['condition_id'] for i in conditions]
                approved = [i for i, e in enumerate(result) if e is True]
                conditions_approved = [str(i) for i in conditions if conditions.index(i) in approved]
                if len(conditions_approved) > 0:
                    await ConditionsInsertCheck.approve_condition(user_id=user_id, condition_id=conditions_approved)
                if len(conditions_approved) == len(conditions):
                    await ConditionsInsertCheck.give_access(user_active_id=user_id, owner_id=owner_id,
                                                            owner_type=owner_type)
            else:
                await ConditionsInsertCheck.give_access(user_active_id=user_id, owner_id=owner_id,
                                                        owner_type=owner_type)
            location = f"{owner_type[1].replace('_id', '')}/{owner_id}"
        return web.HTTPFound(location=str(location))
