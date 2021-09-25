import os
from aiohttp import web
from aiohttp_session import get_session

from config.common import BaseConfig
from models.user import User


class Avatar(web.View):

    async def post(self):
        session = await get_session(self)
        if 'user' not in session:
            return web.HTTPForbidden()

        user = session['user']
        data = await self.post()
        avatar = data['avatar']

        with open(os.path.join(BaseConfig.STATIC_DIR + '/avatars/', avatar.filename), 'wb') as f:
            content = avatar.file.read()
            f.write(content)

        await User.save_avatar_url(user_id=user['id'], url=f"{avatar.filename}")
        location = str(f"/{session['user']['id']}")
        return web.HTTPFound(location=location)
