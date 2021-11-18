import aiohttp_jinja2
from aiohttp import web
from config.common import BaseConfig
from aiohttp_session import get_session
from models.community import Community


class CommunitiesView(web.View):
    @aiohttp_jinja2.template('communities.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()
        user_id = self.session['user']['id']
        communities = await Community.get_user_communities(user_id=user_id)
        return dict(communities=communities)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()
        user_id = self.session['user']['id']
        data = await self.post()
        print(data)
        await Community.create_community(user_id=user_id, data=data)
        return web.HTTPFound(location=self.app.router['community'].url_for())
