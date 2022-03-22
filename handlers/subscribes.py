import aiohttp_jinja2
from aiohttp import web
from models.subscribes import *
import json
from aiohttp.web import json_response


async def get_subscribes_suggestions(request):
    pool = request.app['pool']
    user_id = json.loads(request.cookies['user'])['user_id']
    async with pool.acquire() as conn:
        users = await SubscribesGetInfo.get_user_subscribes_suggestions(user_id=user_id, conn=conn)
    return json_response({'suggestions': users})


async def get_subscribes(request):
    pool = request.app['pool']
    user_id = json.loads(request.cookies['user'])['user_id']
    async with pool.acquire() as conn:
        subscribers = await SubscribesGetInfo.get_subscribers(user_id=user_id, conn=conn)
    friends = [i for i in subscribers if i['status_active'] == 1 and i['status_passive'] == 1]
    subscribers_active = [i for i in subscribers if i['status_passive'] == 1 and i['status_active'] == 0]
    subscribers_passive = [i for i in subscribers if i['status_active'] == 1 and i['status_passive'] == 0]
    blocked = [i for i in subscribers if i['status_active'] == -1]
    return json_response({'friends': friends, 'followers': subscribers_active, 'followings': subscribers_passive,
                          'blocked': blocked})


async def follow(request):
    pool = request.app['pool']
    data = await request.json()
    user_id = json.loads(request.cookies['user'])['user_id']
    user_passive = data['user_passive_id']
    async with pool.acquire() as conn:
        await SubscribesAction.subscribe_user(user_active_id=user_id, user_passive_id=user_passive, conn=conn)
        subscribers = await SubscribesGetInfo.get_subscribers(user_id=user_id, conn=conn)
        friends = [i for i in subscribers if i['status_active'] == 1 and i['status_passive'] == 1]
        subscribers_active = [i for i in subscribers if i['status_passive'] == 1 and i['status_active'] == 0]
        subscribers_passive = [i for i in subscribers if i['status_active'] == 1 and i['status_passive'] == 0]
    return json_response({'value': [friends, subscribers_active, subscribers_passive]})


async def unfollow(request):
    pool = request.app['pool']
    data = await request.json()
    user_id = json.loads(request.cookies['user'])['user_id']
    user_passive = data['user_passive_id']
    async with pool.acquire() as conn:
        await SubscribesAction.unsubscribe_user(user_active_id=user_id, user_passive_id=user_passive, conn=conn)
        subscribers = await SubscribesGetInfo.get_subscribers(user_id=user_id, conn=conn)
        friends = [i for i in subscribers if i['status_active'] == 1 and i['status_passive'] == 1]
        subscribers_active = [i for i in subscribers if i['status_passive'] == 1 and i['status_active'] == 0]
    return json_response({'value': [friends, subscribers_active]})


async def block(request):
    pool = request.app['pool']
    data = await request.json()
    user_id = json.loads(request.cookies['user'])['user_id']
    user_passive = data['user_passive_id']
    async with pool.acquire() as conn:
        await SubscribesAction.block_user(user_active_id=user_id, user_passive_id=user_passive, conn=conn)
        subscribers = await SubscribesGetInfo.get_subscribers(user_id=user_id, conn=conn)
    friends = [i for i in subscribers if i['status_active'] == 1 and i['status_passive'] == 1]
    subscribers_active = [i for i in subscribers if i['status_passive'] == 1 and i['status_active'] == 0]
    subscribers_passive = [i for i in subscribers if i['status_active'] == 1 and i['status_passive'] == 0]
    blocked = [i for i in subscribers if i['status_active'] == -1]
    return json_response({'value': [friends, subscribers_active, subscribers_passive, blocked]})


async def unblock(request):
    pool = request.app['pool']
    data = await request.json()
    user_id = json.loads(request.cookies['user'])['user_id']
    user_passive = data['user_passive_id']
    async with pool.acquire() as conn:
        await SubscribesAction.unblock_user(user_active_id=user_id, user_passive_id=user_passive, conn=conn)
        subscribers = await SubscribesGetInfo.get_subscribers(user_id=user_id, conn=conn)
    friends = [i for i in subscribers if i['status_active'] == 1 and i['status_passive'] == 1]
    subscribers_active = [i for i in subscribers if i['status_passive'] == 1 and i['status_active'] == 0]
    subscribers_passive = [i for i in subscribers if i['status_active'] == 1 and i['status_passive'] == 0]
    blocked = [i for i in subscribers if i['status_active'] == -1]
    return json_response({'value': [friends, subscribers_active, subscribers_passive, blocked]})


class SubscribesView(web.View):

    # @aiohttp_jinja2.template('subscribes.html')
    # async def get(self):
    #     users = await SubscribesGetInfo.get_user_subscribes_suggestions(user_id=json.loads(request.cookies['user'])['user_id'])
    #     return dict(users=users)

    async def post(self):
        data = await self.post()
        await SubscribesAction.subscribe_user(user_active_id=json.loads(request.cookies['user'])['user_id'], user_passive_id=data['uid'])
        location = self.app.router['subscribes'].url_for()
        return web.HTTPFound(location=location)


class MySubscribesView(web.View):

    @aiohttp_jinja2.template('my_subscribes.html')
    async def get(self):
        subscribers = await SubscribesGetInfo.get_subscribers(user_id=json.loads(request.cookies['user'])['user_id'])
        subscribers_active = [i for i in subscribers if i['status_passive'] == 1]
        subscribers_passive = [i for i in subscribers if i['status_active'] == 1]
        blocked = [i for i in subscribers if i['status_active'] == -1]
        return dict(subscribers_active=subscribers_active, subscribers_passive=subscribers_passive, blocked=blocked)

    async def post(self):
        data = await self.post()
        if 'action' in data.keys():
            await SubscribesAction.subscribe_user(user_active_id=json.loads(request.cookies['user'])['user_id'], user_passive_id=data['uid'])
        elif 'unsubscribe' in data.keys() or 'unblock' in data.keys():
            await SubscribesAction.unsubscribe_user(user_active_id=json.loads(request.cookies['user'])['user_id'], user_passive_id=data['uid'])
        elif 'block' in data.keys():
            await SubscribesAction.block_user(user_active_id=json.loads(request.cookies['user'])['user_id'], user_passive_id=data['uid'])
        elif 'unblock' in data.keys():
            await SubscribesAction.unblock_user(user_active_id=json.loads(request.cookies['user'])['user_id'], user_passive_id=data['uid'])
        location = self.app.router['my_subscribes'].url_for()
        return web.HTTPFound(location=location)
