from models.post import Post
from aiohttp import web
from aiohttp_session import get_session
from config.common import BaseConfig
import os
import aiohttp_jinja2


class PostView(web.View):

    async def post(self):
        data = await self.post()
        location = str(f"/{session['user']['id']}")
        if 'user' in session and data['message'] and not data['file']:
            await Post.create_post(user_id=session['user']['id'], message=data['message'])
        if 'user' in session and data['message'] and data['file']:
            data_file = data['file']
            with open(os.path.join(BaseConfig.STATIC_DIR + '/image_posts/', data_file.filename), 'wb') as f:
                content = data_file.file.read()
                f.write(content)
            await Post.create_post(user_id=session['user']['id'], message=data['message'], image_href=data_file.filename)
        return web.HTTPFound(location=location)

    @aiohttp_jinja2.template('posts.html')
    async def get(self):
        location = str(self).split('/')[-1][:-2]
        if location == 'posts':
            posts = await Post.get_posts_subscribes_me(user_id=json.loads(request.cookies['user'])['user_id'])
        elif location == 'my_posts':
            posts = await Post.get_posts_by_user(user_id=json.loads(request.cookies['user'])['user_id'])
        return dict(posts=posts)
