import aiohttp_jinja2
from aiohttp import web
from models.message import Message


class MessageView(web.View):

    @aiohttp_jinja2.template('messages.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()
        users = await Message.get_users_chats(user_id=self.session['user']['id'])
        messages = await Message.get_last_messages(user_id=self.session['user']['id'], user=[i[0] for i in users])
        return dict(messages=messages, users=users)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        await Message.create_message(from_user=self.session['user']['id'],
                                     to_user=data['to_user'], message=data['message_text'])
        location = str(self).split('/')[-1]
        print(location)
        return web.HTTPFound(location=self.app.router[f'chat_{data["to_user"]}'].url_for())
