import aiohttp_jinja2
from aiohttp import web
from models.message import Message
from aiohttp_session import get_session


class ChatView(web.View):

    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()
        friend_id = int(str(self).split('/chat_')[-1][:-2])
        session = await get_session(self)
        message = await Message.get_messages(user_id=session['user']['id'], friend=friend_id)
        return dict(messages=message, friend_id=friend_id, user_id=session['user']['id'])

