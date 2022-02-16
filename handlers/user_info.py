import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.user import *
from models.information import InfoGet
from PIL import Image, ImageDraw
import json
import datetime


class UserInfoView(web.View):

    @aiohttp_jinja2.template('user_info.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())
        countries = await InfoGet.get_countries()
        cities = await InfoGet.get_cities()
        # values = [dict(record) for record in cities]
        # cities = json.dumps(values).replace("</", "<\\/")
        user = await UserGetInfo.get_user_info(self.session['user']['id'])
        conditions = await InfoGet.get_conditions(owner_type=0)
        return dict(countries=countries, cities=cities, user=user, conditions=conditions)

    async def post(self):
        data = await self.post()
        session = await get_session(self)
        data = dict(data)
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

