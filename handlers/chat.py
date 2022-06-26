from models.message import MessageGetInfo
from models.subscribes import SubscribesGetInfo
from models.user import UserGetInfo
import json
from aiohttp.web import json_response


async def get_chat(request):
    pool = request.app['pool']
    chat_id = str(request).split('/chat/')[-1][:-2]
    user_id = json.loads(request.cookies['user'])['user_id']
    block = False
    is_owner = False
    subscribers = None
    participants = None
    async with pool.acquire() as conn:
        messages = await MessageGetInfo.get_messages(chat_id=chat_id, conn=conn)
        if int(user_id) not in messages[0]['participants']:
            return json_response({'forbidden': True})
        if 0 == messages[0]['chat_type']:
            user_passive_id = [i for i in messages[0]['participants'] if int(user_id) != i][0]
            block = await SubscribesGetInfo.is_block(user_active_id=user_id, user_passive_id=user_passive_id, conn=conn)
            chat = await MessageGetInfo.get_user_chat_info(user_id=user_id, chat_id=chat_id, conn=conn)
        elif 1 == messages[0]['chat_type']:
            subscribers = await SubscribesGetInfo.get_user_subscribes_names(user_id=user_id, conn=conn)
            subscribers = [i for i in subscribers if i['user_id'] not in messages[0]['participants']]
            participants = await MessageGetInfo.get_chat_participants(chat_id=chat_id, user_id=user_id, conn=conn)
            chat = await MessageGetInfo.get_group_chat_info(chat_id=chat_id, conn=conn)
        else:
            owner = await MessageGetInfo.is_owner(chat_id=chat_id, conn=conn)
            if owner == int(user_id):
                is_owner = True
            if 2 == messages[0]['chat_type']:
                chat = await MessageGetInfo.get_community_chat_info(chat_id=chat_id, conn=conn)
            elif 3 == messages[0]['chat_type']:
                chat = await MessageGetInfo.get_course_chat_info(chat_id=chat_id, conn=conn)
        avatar = await UserGetInfo.get_avatar_by_user_id(user_id=user_id, conn=conn)
        await MessageGetInfo.is_read(user_id=user_id, chat_id=chat_id, conn=conn)
    return json_response({'messages': messages, 'block': block, 'me': int(user_id),
                          'is_owner': is_owner, 'subscribers': subscribers, 'participants': participants,
                          'chat_info': chat, 'user': avatar[0]})
