import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.user import *
from models.information import InfoGet
from PIL import Image, ImageDraw
import json
import datetime
from aiohttp.web import json_response


async def get_user_info(request):
    pool = request.app['pool']
    cities = None
    async with pool.acquire() as conn:
        user = await UserGetInfo.get_user_info(json.loads(request.cookies['user'])['user_id'], conn=conn)
        countries = await InfoGet.get_countries(conn=conn)
        if user['country_id']:
            cities = await InfoGet.get_cities_by_country(country_id=user['country_id'], conn=conn)

    # conditions = await InfoGet.get_conditions(owner_type=0)
    return json_response({'user': user, 'countries': countries, 'cities': cities})


async def get_cities_by_country(request):
    if str(request).split('/')[-1][:-2] == 'null':
        cities = None
    else:
        pool = request.app['pool']
        async with pool.acquire() as conn:
            cities = await InfoGet.get_cities_by_country(country_id=str(request).split('/')[-1][:-2], conn=conn)
    return json_response({'cities': cities})


async def change_user_info(request):
    data = await request.json()
    print(data)
    pool = request.app['pool']
    if data['table'] == 'user_info':
        del data['table']
        if 'birthday' in data.keys():
            birthday = [int(i) for i in data['birthday'].split('-')]
            today = datetime.date.today()
            data['birthday'] = datetime.date(birthday[0], birthday[1], birthday[2])
            years = today.year - data['birthday'].year
            if today.month < data['birthday'].month or (today.month == data['birthday'].month and
                                                        today.day < data['birthday'].day):
                years -= 1
            data['age'] = years
        async with pool.acquire() as conn:
            await UserCreate.create_user_info(user_id=json.loads(request.cookies['user'])['user_id'], data=data,
                                              conn=conn)
    elif data['table'] == 'user_main':
        del data['table']
        async with pool.acquire() as conn:
            await UserCreate.create_user_main(user_id=json.loads(request.cookies['user'])['user_id'], data=data,
                                              conn=conn)

    return json_response({'response': 200})


class UserInfoView(web.View):
    async def post(self):
        data = await self.post()
        session = await get_session(self)
        data = dict(data)
        # todo: image, percentage
        user_id = session['user']['id']
        # data['birthday'] = [int(i) for i in data['birthday'].split('-')]
        # data['birthday'] = datetime.date(data['birthday'][0], data['birthday'][1], data['birthday'][2])
        keys = [i for i in data.keys()]
        keys_conditions = keys[keys.index('bio')+1:]
        data_new = {'condition_id': [], 'task': [], 'answers': [], 'condition_value': [], 'images': []}
        for i in keys_conditions:
            if 'select_condition' in i:
                data_new['condition_id'] += [data[i]]
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
                    path = f'static/conditions/condition_{user_id}{data[text]}.jpg'
                    img.save(path)
                    data_new['images'] += [path.replace('static/conditions/', '')]
                else:
                    data_new['images'] += ['null']
        for i in keys_conditions:
            del data[i]
        user_info = await UserCreate.get_user_info(user_id)
        drop = []
        for i in data.keys():
            if data[i] == user_info[i]:
                drop.append(i)
        for i in drop:
            del data[i]
        await UserCreate.create_user_info(user_id=user_id, data=data)
        await UserCreate.create_user_info_conditions(user_id=user_id, data=data_new)
        return web.HTTPFound(location=f"/user/{session['user']['id']}")

