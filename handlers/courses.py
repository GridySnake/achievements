import aiohttp_jinja2
from aiohttp import web
from models.course import *
from models.information import InfoGet
from models.community import CommunityGetInfo
import os
from models.subscribes import SubscribesGetInfo
from models.goal import Goals
from PIL import Image, ImageDraw
from models.conditions import ConditionsGetInfo
import json
from config.common import BaseConfig
from aiohttp.web import json_response
from models.images import Images


async def get_courses(request):
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    async with pool.acquire() as conn:
        own_courses = await CoursesGetInfo.get_own_courses(user_id=user_id, conn=conn)
        # communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id)
        # languages = await InfoGet.get_languages()
        my_courses = await CoursesGetInfo.get_user_courses(user_id=user_id, conn=conn)
        sug_courses = await CoursesGetInfo.get_user_course_suggestions(user_id=user_id, conn=conn)
        assis_course = await CoursesGetInfo.get_assistant_courses(user_id=user_id, conn=conn)
        requests = await CoursesGetInfo.user_requests(user_id=user_id, conn=conn)
        completed_courses = await CoursesGetInfo.get_completed_courses(user_id=user_id, conn=conn)
        communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id, conn=conn)
        spheres = await InfoGet.get_spheres(conn=conn)
        currencies = await InfoGet.get_currencies(conn=conn)
        languages = await InfoGet.get_languages(conn=conn)
    # subspheres = await InfoGet.get_subspheres()
    # conditions = await InfoGet.get_conditions(owner_type=2)
    return json_response({'sug_courses': sug_courses, 'own_courses': own_courses, 'progress': my_courses,
                          'complete': completed_courses, 'assistant_courses': assis_course, 'requests': requests,
                          'create': {'communities': communities, 'spheres': spheres, 'currencies': currencies,
                                     'languages': languages}})


async def get_course_info(request):
    course_id = str(request).split('/')[-1][:-2]
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    async with pool.acquire() as conn:
        goals = await Goals.get_goals(user_id=course_id, user_type=2, conn=conn)
        course = await CoursesGetInfo.get_course_info(course_id=course_id, conn=conn)
        in_course = await CoursesGetInfo.is_user_in_course(course_id=course_id, user_id=user_id, conn=conn)
        participants = await CoursesGetInfo.get_course_participants(course_id=course_id, conn=conn)
        owner = await CoursesGetInfo.is_owner(course_id=course_id, user_id=user_id, conn=conn)
        subscribers = None
        allow = True
        conditions = False
        if not in_course:
            can_join = await ConditionsGetInfo.is_allowed_communicate_by_conditions(user_active_id=user_id,
                                                                                    user_passive_id=course_id,
                                                                                    owner_table='courses',
                                                                                    owner_column='course_id',
                                                                                    conn=conn)
            if not can_join:
                conditions = await CoursesGetInfo.get_course_conditions(user_id=user_id, course_id=course_id, conn=conn)
                allow = False
        if owner:
            subscribers = await SubscribesGetInfo.get_user_subscribes_names(user_id=user_id, conn=conn)
            subscribers = [i for i in subscribers if subscribers and
                           i['user_id'] not in [j['user_id'] for j in participants if participants]]
    return json_response({'course': course, 'in_course': in_course, 'owner': owner, 'subscribers': subscribers,
                          'participants': participants, 'goals': goals, 'conditions': conditions, 'allow': allow})


async def join_course(request):
    data = await request.json()
    course_id = data['course_id']
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    async with pool.acquire() as conn:
        await CoursesAction.join_course(course_id=course_id, user_id=user_id, conn=conn)
    return json_response({'value': f'join_{course_id}'})


async def leave_course(request):
    data = await request.json()
    course_id = data['course_id']
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    async with pool.acquire() as conn:
        await CoursesAction.leave_course(course_id=course_id, user_id=user_id, conn=conn)
    return json_response({'value': f'leave_{course_id}'})


async def add_course_member(request):
    data = await request.json()
    course_id = data['course_id']
    pool = request.app['pool']
    users = data['users']
    status = ['1' for i in range(len(users))]
    async with pool.acquire() as conn:
        await CoursesAction.add_member(course_id=course_id, users=users, status=status, conn=conn)
    return json_response({'value': f'add_member_{course_id}_{"".join(users)}'})


async def accept_course(request):
    data = await request.json()
    course_id = data['course_id']
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    action = 1
    async with pool.acquire() as conn:
        await CoursesAction.accept_decline_request(user_id=user_id, action=action, course_id=course_id, conn=conn)
    return json_response({'value': f'accepted_{course_id}'})


async def decline_course(request):
    data = await request.json()
    course_id = data['course_id']
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    action = 0
    async with pool.acquire() as conn:
        await CoursesAction.accept_decline_request(user_id=user_id, action=action, course_id=course_id, conn=conn)
    return json_response({'value': f'declined_{course_id}'})


async def upload_course_avatar(request):
    try:
        data = await request.multipart()
        d = await data.next()
        with open(os.path.join(BaseConfig.STATIC_DIR + '/course_avatar/' + d.filename), 'wb') as f:
            chunk = await d.read_chunk()
            f.write(chunk)
    except:
        return json_response({'image_id': None})
    pool = request.app['pool']
    async with pool.acquire() as conn:
        image_id = await Images.create_image(path=d.filename, image_type='course', conn=conn)
    return json_response({'image_id': image_id})


async def create_course(request):
    data = await request.json()
    if data['type'] == 0:
        user_id = json.loads(request.cookies['user'])['user_id']
    else:
        user_id = data['user_id']
    pool = request.app['pool']
    print(data)
    no_image = False
    if data['avatar'] is None:
        no_image = True
    async with pool.acquire() as conn:
        course_id = await CourseCreate.create_course(user_id=user_id, data=data, no_image=no_image, conn=conn)
    return json_response({'course': course_id})


async def course_content(request):
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    course_id = str(request).split('/')[-1][:-2]
    async with pool.acquire() as conn:
        # count = await CourseContentModel.count_course_content(course_id=course_id, conn=conn)
        # content_table = await CourseContentModel.course_content_table(course_id=course_id, conn=conn)
        navigation = await CourseContentModel.course_content_navigation(course_id=course_id, conn=conn)
    return json_response({'navigation': navigation})


async def course_content_task(request):
    pool = request.app['pool']
    course_id = str(request).split('/')[-3]
    page = str(request).split('/')[-1][:-2]
    async with pool.acquire() as conn:
        content = await CourseContentModel.course_content_page(course_id=course_id, page=page, conn=conn)
    return json_response({'content': content})


class CoursesView(web.View):

    @aiohttp_jinja2.template('courses.html')
    async def get(self):
        user_id = json.loads(request.cookies['user'])['user_id']
        own_courses = await CoursesGetInfo.get_own_courses(user_id=user_id)
        communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id)
        languages = await InfoGet.get_languages()
        courses = await CoursesGetInfo.get_user_course_suggestions(user_id=user_id)
        my_courses = await CoursesGetInfo.get_user_courses(user_id=user_id)
        sug_courses = await CoursesGetInfo.get_user_course_suggestions(user_id=user_id, conn=conn)
        requests = await CoursesGetInfo.user_requests(user_id=user_id)
        subspheres = await InfoGet.get_subspheres()
        conditions = await InfoGet.get_conditions(owner_type=2)
        return dict(courses=courses, my_courses=my_courses, languages=languages, communities=communities, own_courses=own_courses, requests=requests, subspheres=subspheres, conditions=conditions)

    async def post(self):

        user_id = json.loads(request.cookies['user'])['user_id']
        data = await self.post()
        avatar = data['avatar']
        data = dict(data)
        if 'online' in data.keys():
            data['online'] = True
        else:
            data['online'] = False
        if 'free' in data.keys():
            data['free'] = True
        else:
            data['free'] = False
        if 'as_community' in data.keys():
            data['type'] = 1
            user_id = data['community']
        else:
            data['type'] = 0
            user_id = json.loads(request.cookies['user'])['user_id']
        no_image = False
        if data['avatar'] == bytearray(b''):
            no_image = True
        else:
            with open(os.path.join(BaseConfig.STATIC_DIR + '/course_avatar/', avatar.filename), 'wb') as f:
                content = avatar.file.read()
                f.write(content)
            data['avatar'] = avatar.filename
        data['sphere'] = await InfoGet.get_sphere_id_by_subsphere_id(data['select_subsphere'])
        course_id = await CourseCreate.create_course(user_id=user_id, data=data, no_image=no_image)
        keys = [i for i in data.keys()]
        keys_conditions = keys[keys.index('select_condition0') : keys.index('background_color1')+1]
        data_new = {'condition_id': [], 'task': [], 'answers': [], 'condition_value': [], 'images': []}
        for i in keys_conditions:
            if 'select_condition' in i:
                data_new['condition_id'] += [data[i]]
                print(data[i])
            if 'task' in i:
                if data[i] == '':
                    data_new['task'] += ['null']
                else:
                    data_new['task'] += [data[i]]
            if 'answers' in i:
                if data[i] == '':
                    data_new['answers'] += ['null']
                else:
                    data_new['answers'] += [data[i]]
            if 'condition_value' in i:
                if data[i] == '':
                    data_new['condition_value'] += ['null']
                else:
                    data_new['condition_value'] += [data[i]]
            if 'text_color' in i:
                if data[i] != '#000000':
                    num = i.replace('text_color', '')
                    back = 'background_color' + num
                    img = Image.new('RGB', (100, 30), color=data[back])
                    text = 'task' + num
                    d = ImageDraw.Draw(img)
                    d.text((10, 10), data[text], fill=data[i])
                    path = f'static/conditions/condition_course_{course_id}{data[text]}.jpg'
                    img.save(path)
                    data_new['images'] += [path.replace('static/conditions/', '')]
                else:
                    data_new['images'] += ['null']
            await CourseCreate.create_course_info_conditions(course_id=course_id, data=data_new)
        return web.HTTPFound(location='/courses')


class CourseInfoView(web.View):

    @aiohttp_jinja2.template('course_info.html')
    async def get(self):

        # todo : убрать из subscribers тех, кому уже отправлено приглашение
        course_id = str(self).split('/')[-1][:-2]
        user_id = json.loads(request.cookies['user'])['user_id']
        goals = await Goals.get_goals(user_id=course_id, user_type=2)
        course = await CoursesGetInfo.get_course_info(course_id=course_id)
        in_course = await CoursesGetInfo.is_user_in_course(course_id=course_id, user_id=user_id)
        participants = await CoursesGetInfo.get_course_participants(course_id=course_id)
        subscribers = None
        #spheres = await InfoGet.get_spheres_subspheres_by_id(subspheres_id=[i for i in course['subsphere_id']])
        owner = await CoursesGetInfo.is_owner(course_id=course_id, user_id=user_id)
        allow = True
        conditions = False
        if not in_course:
            can_join = await ConditionsGetInfo.is_allowed_communicate_by_conditions(user_active_id=user_id,
                                                                                    user_passive_id=course_id,
                                                                                    owner_table=
                                                                                    'courses',
                                                                                    owner_column='course_id')
            if not can_join:
                conditions = await CoursesGetInfo.get_course_conditions(user_id=user_id, course_id=course_id)
                allow = False
        if owner:
            subscribers = await SubscribesGetInfo.get_user_subscribes_names(user_id=user_id)
            subscribers = [i for i in subscribers if i['user_id'] not in [j['user_id'] for j in participants]]
        return dict(course=course, in_course=in_course, owner=owner, subscribers=subscribers, participants=participants,
                    goals=goals, conditions=conditions, allow=allow)

    async def post(self):

        course_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('course/')[1][:-2]

        user_id = json.loads(request.cookies['user'])['user_id']
        data = await self.post()
        if 'join' in data.keys():
            await CoursesAction.join_course(course_id=course_id, user_id=user_id)
        elif 'leave' in data.keys():
            await CoursesAction.leave_course(course_id=course_id, user_id=user_id)
        elif 'add_course_member' in str(self):
            users = [int(i) for i in data.keys()]
            status = [1 for i in range(len(users))]
            await CoursesAction.add_member(course_id=course_id, users=users, status=status)
        return web.HTTPFound(location='/courses')


class CourseContent(web.View):
    @aiohttp_jinja2.template('course_content.html')
    async def get(self):

        course_id = str(self).split('/')[2]
        page = str(self).split('/course_content/')[-1][:-2]
        count = await CourseContentModel.count_course_content(course_id=course_id)
        page_content = await CourseContentModel.course_content_page(course_id=course_id, page=page)
        navigation = await CourseContentModel.course_content_navigation(course_id=course_id)
        return dict(count=count, page_content=page_content, navigation=navigation, page=int(page), course_id=course_id)


class CourseContentCreate(web.View):
    @aiohttp_jinja2.template('course_create_content.html')
    async def get(self):

        return dict()

    async def post(self):

        data = await self.post()
        course_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/')[-1][:-2]
        content = {'name': [], 'description': [], 'type': [], 'page': []}
        for i in data.keys():
            if 'name' in i:
                content['name'].append(data[i])
            elif 'description' in i:
                content['description'].append(data[i])
            elif 'type' in i:
                content['type'].append(data[i])
            elif 'page' in i:
                content['page'].append(data[i])
        chapters = [False for i in range(len(content['name']))]
        if len([i for i in data.keys() if 'chapter' in i and 'sub' not in i]) > 0:
            for j in [int(i.replace('chapter', '')) for i in data.keys() if 'chapter' in i and 'sub' not in i]:
                chapters[j] = True
        content['chapter'] = chapters
        subchapters = [False for i in range(len(content['name']))]
        if len([i for i in data.keys() if 'subchapter' in i]) > 0:
            for j in [int(i.replace('subchapter', '')) for i in data.keys() if 'subchapter' in i]:
                subchapters[j] = True
        content['subchapter'] = subchapters
        paths = ['' for i in range(len(content['name']))]
        for i in range(len(content['type'])):
            if content['type'][i] == 'photo':
                photo = data[f'file{i}']
                with open(os.path.join(BaseConfig.STATIC_DIR + f'/course_content/course_{course_id}', photo.filename), 'wb') as f:
                    contents = photo.file.read()
                    f.write(contents)
                paths[i] = photo.filename
            elif content['type'][i] == 'video':
                video = data[f'file{i}']
                with open(os.path.join(BaseConfig.STATIC_DIR + f'/course_content/course_{course_id}', video.filename), 'wb') as f:
                    contents = video.file.read()
                    f.write(contents)
                paths[i] = video.filename
            elif content['type'][i] == 'document':
                doc = data[f'file{i}']
                with open(os.path.join(BaseConfig.STATIC_DIR + f'/course_content/course_{course_id}', doc.filename), 'wb') as f:
                    contents = doc.file.read()
                    f.write(contents)
                paths[i] = doc.filename
            elif content['type'][i] == 'PDF':
                pdf = data[f'file{i}']
                with open(os.path.join(BaseConfig.STATIC_DIR + f'/course_content/course_{course_id}', pdf.filename), 'wb') as f:
                    contents = pdf.file.read()
                    f.write(contents)
                    paths[i] = pdf.filename
            elif content['type'][i] == 'test':
                print('test')
        content['path'] = paths
        await CourseContentModel.course_create_content(course_id=course_id, content=content)
        return web.HTTPFound(location=f'/course/{course_id}')
