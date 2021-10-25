from models.post import Post
from aiohttp import web
from aiohttp_session import get_session
from config.common import BaseConfig
import os


class PostView(web.View):

    async def post(self):
        data = await self.post()
        session = await get_session(self)
        if 'user' not in self.session:
            return web.HTTPForbidden()
        if 'user' in session and data['message'] and not data['file']:
            await Post.create_post(user_id=session['user']['id'], message=data['message'])
        if 'user' in session and data['message'] and data['file']:
            data_file = data['file']
            with open(os.path.join(BaseConfig.STATIC_DIR + '/image_posts/', data_file.filename), 'wb') as f:
                content = data_file.file.read()
                f.write(content)
            await Post.create_post(user_id=session['user']['id'], message=data['message'], image_href=data_file.filename)
            location = str(f"/{session['user']['id']}")
            return web.HTTPFound(location=location)

