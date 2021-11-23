import aiohttp_jinja2
from aiohttp import web
from models.community import Community
import os
from config.common import BaseConfig


class CommunitiesView(web.View):
    @aiohttp_jinja2.template('communities.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        user_id = self.session['user']['id']
        owner_communities = await Community.get_user_owner_communities(user_id=user_id)
        communities = await Community.get_user_communities(user_id=user_id)
        return dict(communities=communities, owner_communities=owner_communities)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        user_id = self.session['user']['id']
        data = await self.post()
        await Community.create_community(user_id=user_id, data=data)
        return web.HTTPFound(location=self.app.router['community'].url_for())


class CommunitiesInfoView(web.View):
    @aiohttp_jinja2.template('community_info.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        community_id = str(self).split('/community/')[-1][:-2]
        community = await Community.get_community_info(community_id=community_id)
        access = False
        print(community)
        if self.session['user']['id'] in [int(i['community_owner_id']) for i in community]:
            access = True
        is_in_community = False
        try:
            if self.session['user']['id'] in [int(i['user_id']) for i in community if community]:
                is_in_community = True
        except:
            None
        return dict(community=community[0], access=access, in_community=is_in_community)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        data = await self.post()
        community_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/community/')[1][:-2]
        location = str(f"/community/{community_id}")
        if 'community_avatar' in data:
            community_avatar = data['community_avatar']

            with open(os.path.join(BaseConfig.STATIC_DIR + '/community_avatar/', community_avatar.filename), 'wb') as f:
                content = community_avatar.file.read()
                f.write(content)

            await Community.save_community_avatar_url(community_id=community_id, url=f"{community_avatar.filename}")
        else:
            method = str(self).split('/')[1][:-2].split('_')[0]
            user_id = self.session['user']['id']
            await Community.leave_join(community_id=community_id, user_id=user_id, method=method)

        return web.HTTPFound(location=location)
