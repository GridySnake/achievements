from models.post import Post
from aiohttp import web
from aiohttp_session import get_session


class PostView(web.View):

    async def post(self):
        data = await self.post()
        session = await get_session(self)
        if 'user' in session and data['message']:
            await Post.create_post(user_id=session['user']['id'], message=data['message'])
            location = str(f"/{session['user']['id']}")
            return web.HTTPFound(location=location)
        return web.HTTPForbidden()
