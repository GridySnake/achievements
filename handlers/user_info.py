import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.user import User


class UserInfoView(web.View):

    @aiohttp_jinja2.template('user_info.html')
    async def get(self):
        return dict()

    async def post(self):
        data = await self.post()
        session = await get_session(self)
        if data['age'] and data['name'] and data['surname']:
            data = dict(data)
            data['id'] = session['user']['id']
            await User.create_user_info(data)
        else:
            return web.HTTPNotFound()
        location = str(f"/{session['user']['id']}")
        return web.HTTPFound(location=location)
