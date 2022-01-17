import aiohttp_jinja2
from aiohttp import web
from models.message import MessageGetInfo
from models.subscribes import SubscribesGetInfo
from aiohttp_session import get_session


class ChatView(web.View):

    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        chat_id = str(self).split('/chat/')[-1][:-2]
        session = await get_session(self)
        messages = await MessageGetInfo.get_messages(chat_id=chat_id)
        block = False
        is_owner = False
        if 0 in [i['chat_type'] for i in messages]:
            user_passive_id = [i for i in messages[0]['participants'] if int(session['user']['id']) != i][0]
            block = await SubscribesGetInfo.is_block(user_active_id=session['user']['id'], user_passive_id=user_passive_id)
        elif 1 in [i['chat_type'] for i in messages]:
            None
        else:
            owner = await MessageGetInfo.is_owner(chat_id=chat_id)
            if owner == session['user']['id']:
                is_owner = True
        await MessageGetInfo.is_read(user_id=session['user']['id'], chat_id=chat_id)
        return dict(messages=messages, chat_id=chat_id, user_id=session['user']['id'], block=block, is_owner=is_owner)

