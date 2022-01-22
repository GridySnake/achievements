import aiohttp_jinja2
from aiohttp import web
from models.community import *
import os
from models.subscribes import SubscribesGetInfo
from config.common import BaseConfig
import json


class CommunitiesView(web.View):
    @aiohttp_jinja2.template('communities.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        conditions = await CommunityGetInfo.get_generate_conditions()
        community_types = set([i['community_type'] for i in conditions])
        values = [dict(record) for record in conditions]
        dropdown_community = json.dumps(values).replace("</", "<\\/")
        user_id = self.session['user']['id']
        owner_communities = await CommunityGetInfo.get_user_owner_communities(user_id=user_id)
        communities = await CommunityGetInfo.get_user_communities(user_id=user_id)
        requests = await CommunityGetInfo.user_requests(user_id=user_id)
        return dict(communities=communities, owner_communities=owner_communities, conditions=conditions, community_types=community_types, dropdown_community=dropdown_community, requests=requests)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        user_id = self.session['user']['id']
        if 'invitation_community' in str(self):
            community_id = str(self).split('/')[-1][:-2]
            action = 0
            if 'accept' in str(self):
                action = 1
            await CommunityAvatarAction.accept_decline_request(user_id=user_id, action=action, community_id=community_id)
        else:
            data = await self.post()
            await CommunityCreate.create_community(user_id=user_id, data=data)

        return web.HTTPFound(location=self.app.router['community'].url_for())


class CommunitiesInfoView(web.View):
    @aiohttp_jinja2.template('community_info.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        community_id = str(self).split('/community/')[-1][:-2]
        community = await CommunityGetInfo.get_community_info(community_id=community_id)
        access = False
        participants = await CommunityGetInfo.get_community_participants(community_id=community_id)
        participants_for_remove = None
        subscribers = None
        if type(community['community_owner_id']) == int:
            if self.session['user']['id'] == community['community_owner_id']:
                access = True
                subscribers = await SubscribesGetInfo.get_user_subscribes_names(user_id=self.session['user']['id'])
                participants_for_remove = [i for i in participants if i['user_id'] != self.session['user']['id']]
        else:
            if self.session['user']['id'] in community['community_owner_id']:
                access = True
                subscribers = await SubscribesGetInfo.get_user_subscribes_names(user_id=self.session['user']['id'])
                participants_for_remove = [i for i in participants if i['user_id'] != self.session['user']['id']]
        is_in_community = False
        if type(community['user_id']) == int:
            if self.session['user']['id'] ==  community['user_id']:
                is_in_community = True
        else:
            if self.session['user']['id'] in [i['user_id'] for i in community]:
                is_in_community = True
        return dict(community=community, access=access, in_community=is_in_community, subscribers=subscribers, participants=participants, participants_for_remove=participants_for_remove)

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

            await CommunityAvatarAction.save_community_avatar_url(community_id=community_id, url=f"{community_avatar.filename}")
        if 'add_community_member' in str(self):
            users = [int(i) for i in data.keys()]
            status = [i for i in range(len(users))]
            community = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/community/')[-1][:-2]
            await CommunityAvatarAction.add_member(community_id=community, users=users, status=status)
        elif 'delete_community_member' in str(self):
            users = [int(i) for i in data.keys()]
            community = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/community/')[-1][:-2]
            await CommunityAvatarAction.remove_member(community_id=community, users=users)
        else:
            method = str(self).split('/')[1][:-2].split('_')[0]
            user_id = self.session['user']['id']
            await CommunityAvatarAction.leave_join(community_id=community_id, user_id=user_id, method=method)

        return web.HTTPFound(location=location)
