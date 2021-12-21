import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.user import UserCreate
from models.information import InfoGet
import json


class UserInfoView(web.View):

    @aiohttp_jinja2.template('user_info.html')
    async def get(self):
        countries = await InfoGet.get_countries()
        cities = await InfoGet.get_cities()
        values = [dict(record) for record in cities]
        cities = json.dumps(values).replace("</", "<\\/")
        return dict(countries=countries, cities=cities)

    async def post(self):
        data = await self.post()
        session = await get_session(self)
        if data['age'] and data['name'] and data['surname']:
            data = dict(data)
            data['id'] = session['user']['id']
            await UserCreate.create_user_info(data)
        else:
            return web.HTTPNotFound()
        location = str(f"/{session['user']['id']}")
        return web.HTTPFound(location=location)

