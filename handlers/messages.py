import aiohttp_jinja2
from aiohttp import web
from models.message import *
import json


class MessageView(web.View):

    @aiohttp_jinja2.template('messages.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        user_chats = await MessageGetInfo.get_users_chats(user_id=self.session['user']['id'])
        community_chats = await MessageGetInfo.get_community_chats(user_id=self.session['user']['id'])
        course_chats = await MessageGetInfo.get_course_chats(user_id=self.session['user']['id'])
        all_chats = [i for i in user_chats] + [i for i in community_chats] + [i for i in course_chats]
        values = [dict(record) for record in all_chats]
        chats_json = json.dumps(values).replace("</", "<\\/")
        messages = await MessageGetInfo.get_last_messages(user_id=self.session['user']['id'], user=[i[0] for i in user_chats])
        print(chats_json)
        return dict(messages=messages, users=user_chats, chats_json=chats_json, communities=community_chats)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        type1 = '0'
        type2 = '0'
        data = await self.post()
        to_user = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('8080/')[1][:-2].split('_')[1]
        await MessageCreate.create_message(from_user=self.session['user']['id'],
                                     to_user=to_user, message=data['message_text'], type1=type1, type2=type2)

        return web.HTTPFound(location=self.app.router[f'chat_{to_user}'].url_for())
