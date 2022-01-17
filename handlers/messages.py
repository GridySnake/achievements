import aiohttp_jinja2
from aiohttp import web
from models.message import *
import json
import os


class MessageView(web.View):

    @aiohttp_jinja2.template('messages.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        user_chats = await MessageGetInfo.get_users_chats(user_id=self.session['user']['id'])
        community_chats = await MessageGetInfo.get_community_chats(user_id=self.session['user']['id'])
        course_chats = await MessageGetInfo.get_course_chats(user_id=self.session['user']['id'])
        group_chats = await MessageGetInfo.get_group_chats(user_id=self.session['user']['id'])

        # all_chats = [i for i in user_chats] + [i for i in community_chats] + [i for i in course_chats]
        # values = [dict(record) for record in all_chats]
        # chats_json = json.dumps(values).replace("</", "<\\/")
        # print(chats_json)
        return dict(users=user_chats, communities=community_chats, courses=course_chats, groups=group_chats)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        if 'send_message' in str(self):

            data = await self.post()
            from_user = self.session['user']['id']
            type1 = '0'
            chat_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/chat/')[-1][:-2]
            if 'community_message' in data.keys():
                type1 = '2'
                from_user = await MessageGetInfo.get_chat_owner_cc(chat_id=chat_id)
            elif 'course_message' in data.keys():
                type1 = '3'
                from_user = await MessageGetInfo.get_chat_owner_cc(chat_id=chat_id)
            await MessageCreate.create_message(from_user=from_user, message=data['message_text'],
                                               type1=type1, chat_id=chat_id)
        else:
            data = await self.post()
            if data['group_chat_avatar'] != bytearray(b''):
                group_chat_avatar = data['group_chat_avatar']
                with open(os.path.join(BaseConfig.STATIC_DIR + '/group_avatar/', group_chat_avatar.filename),
                          'wb') as f:
                    content = group_chat_avatar.file.read()
                    f.write(content)
                chat_id = await MessageCreate.create_group_chat(owner_id=self.session['user']['id'],
                                                                chat_name=data['group_chat_name'],
                                                                chat_avatar=group_chat_avatar.filename)
            else:
                chat_id = await MessageCreate.create_group_chat(owner_id=self.session['user']['id'],
                                                                chat_name=data['group_chat_name'])

        return web.HTTPFound(location=f'/chat/{chat_id}')
