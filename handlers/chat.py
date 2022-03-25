from models.message import MessageGetInfo
from models.subscribes import SubscribesGetInfo
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
        if 0 in [i['chat_type'] for i in messages]:
            user_passive_id = [i for i in messages[0]['participants'] if int(user_id) != i][0]
            block = await SubscribesGetInfo.is_block(user_active_id=user_id, user_passive_id=user_passive_id, conn=conn)
            print(user_passive_id)
        elif 1 in [i['chat_type'] for i in messages]:
            subscribers = await SubscribesGetInfo.get_user_subscribes_names(user_id=user_id, conn=conn)
            participants = [i for i in messages[0]['participants'] if i != int(user_id)]
            subscribers = [i for i in subscribers if i['user_id'] not in participants]
            participants = await MessageGetInfo.get_chat_participants(chat_id=chat_id, user_id=user_id, conn=conn)
        else:
            owner = await MessageGetInfo.is_owner(chat_id=chat_id, conn=conn)
            if owner == int(user_id):
                is_owner = True

        await MessageGetInfo.is_read(user_id=user_id, chat_id=chat_id, conn=conn)
    return json_response({'messages': messages, 'block': block, 'me': int(user_id),
                          'is_owner': is_owner, 'subscribers': subscribers, 'participants': participants})
