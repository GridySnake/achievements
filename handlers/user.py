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
        if data['age'] and data['name'] and data['surname']:
            await User.create_user_info(data)
        else:
            return web.HTTPNotFound()
        session = await get_session(self)
        location = str(f"/{session['user']['id']}")
        return web.HTTPFound(location=location)

