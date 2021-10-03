import aiohttp_jinja2
from aiohttp import web
from models.friends import Friends


class FriendsView(web.View):

    @aiohttp_jinja2.template('friends.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        users = await Friends.get_user_friends_suggestions(user_id=self.session['user']['id'])
        return dict(users=users)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        await Friends.add_friend(user_active_id=self.session['user']['id'], user_passive_id=data['uid'])
        location = self.app.router['friends'].url_for()
        return web.HTTPFound(location=location)


class MyFriendsView(web.View):

    @aiohttp_jinja2.template('my_friends.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()
        users = await Friends.get_user_friends_names(user_id=self.session['user']['id'])
        subscribers = await Friends.get_subscribers(user_id=self.session['user']['id'])
        actual_requests = [i for i in subscribers if i['status_id_active'] == 2 and i['status_id_passive'] != -1]
        subscribers_active = [i for i in subscribers if i['status_id_active'] == 2 and i['status_id_passive'] == -1]
        subscribers_passive = [i for i in subscribers if i['status_id_active'] == 0]
        print(actual_requests, subscribers_active, subscribers_passive)
        return dict(users=users, subscribers_active=subscribers_active, subscribers_passive=subscribers_passive, actual_requests=actual_requests)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        await Friends.friends_confirm(user_active_id=self.session['user']['id'], user_passive_id=data['uid'], confirm=eval(data['action']))
        location = self.app.router['my_friends'].url_for()
        return web.HTTPFound(location=location)
