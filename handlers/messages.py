from aiohttp import web
from models.message import *
import json
import os
from aiohttp.web import json_response


async def messages(request):
    user_id = json.loads(request.cookies['user'])['user_id']
    pool = request.app['pool']
    async with pool.acquire() as conn:
        user_chats = await MessageGetInfo.get_users_chats(user_id=user_id, conn=conn)
        community_chats = await MessageGetInfo.get_community_chats(user_id=user_id, conn=conn)
        course_chats = await MessageGetInfo.get_course_chats(user_id=user_id, conn=conn)
        group_chats = await MessageGetInfo.get_group_chats(user_id=user_id, conn=conn)
    return json_response({'users': user_chats, 'groups': group_chats, 'communities': community_chats,
                          'courses': course_chats})


async def send_message(request):
    if 'send_message' in str(request):

        data = await request.json()
        from_user = json.loads(request.cookies['user'])['user_id']
        type1 = '0'
        chat_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/chat/')[-1][:-2]
        if '/user/' in str(self.__dict__['_message']).split('Referer')[-1].split(',')[1]:
            user_id1 = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/user/')[-1][:-2]
            chat_id = await MessageGetInfo.get_chat(user_id=from_user, user_id1=user_id1)
            await MessageCreate.create_message(from_user=from_user, message=data['message_text'],
                                               type1=type1, chat_id=chat_id, to_user=user_id1)
            chat_id = await MessageGetInfo.get_chat(user_id=from_user, user_id1=user_id1)
        else:
            if 'community_message' in data.keys():
                type1 = '2'
                from_user = await MessageGetInfo.get_chat_owner_cc(chat_id=chat_id)
            elif 'course_message' in data.keys():
                type1 = '3'
                from_user = await MessageGetInfo.get_chat_owner_cc(chat_id=chat_id)
            await MessageCreate.create_message(from_user=from_user, message=data['message_text'],
                                               type1=type1, chat_id=chat_id)
    elif 'add_member' in str(self):
        data = await self.post()
        users = [int(i) for i in data.keys()]
        chat_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/chat/')[-1][:-2]
        await MessageCreate.add_member(chat_id=chat_id, users=users)

    elif 'remove_member' in str(self):
        data = await self.post()
        users = [int(i) for i in data.keys()]
        chat_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/chat/')[-1][:-2]
        await MessageCreate.remove_member(chat_id=chat_id, users=users)

    else:
        data = await self.post()
        if data['group_chat_avatar'] != bytearray(b''):
            group_chat_avatar = data['group_chat_avatar']
            with open(os.path.join(BaseConfig.STATIC_DIR + '/group_avatar/', group_chat_avatar.filename),
                      'wb') as f:
                content = group_chat_avatar.file.read()
                f.write(content)
            chat_id = await MessageCreate.create_group_chat(owner_id=json.loads(request.cookies['user'])['user_id'],
                                                            chat_name=data['group_chat_name'],
                                                            chat_avatar=group_chat_avatar.filename)
        else:
            chat_id = await MessageCreate.create_group_chat(owner_id=json.loads(request.cookies['user'])['user_id'],
                                                            chat_name=data['group_chat_name'])

    return web.HTTPFound(location=f'/chat/{chat_id}')
