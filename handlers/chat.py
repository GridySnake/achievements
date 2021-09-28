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
        inbox = await Message.get_inbox_messages_by_user(user_id=self.session['user']['id'], friend=friend_id)
        outbox = await Message.get_send_messages_by_user(user_id=self.session['user']['id'], friend=friend_id)
        message = inbox + outbox
        session = await get_session(self)
        return dict(messages=message, friend_id=friend_id, user_id=session['user']['id'])

