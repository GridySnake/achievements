import aiohttp_jinja2
from aiohttp import web
from models.subscribes import *


class SubscribesView(web.View):

    @aiohttp_jinja2.template('subscribes.html')
    async def get(self):
        users = await SubscribesGetInfo.get_user_subscribes_suggestions(user_id=json.loads(request.cookies['user'])['user_id'])
        return dict(users=users)

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
