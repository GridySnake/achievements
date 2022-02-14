import aiohttp_jinja2
from aiohttp import web
from models.community import *
import os
from models.subscribes import SubscribesGetInfo
from config.common import BaseConfig
import numpy as np
import json
from models.information import InfoGet
from models.goal import Goals
from models.wallet_community_goal import *
from PIL import Image, ImageDraw


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
        subspheres = await InfoGet.get_subspheres()
        communities_recommend = await CommunityGetInfo.get_some_communities(user_id=user_id)
        conditions_to_join = await InfoGet.get_conditions(owner_type=1)
        return dict(communities=communities, owner_communities=owner_communities,
                    conditions=conditions,
                    community_types=community_types,
                    dropdown_community=dropdown_community,
                    requests=requests,
                    subspheres=subspheres,
                    communities_recommend=communities_recommend, conditions_tj=conditions_to_join)

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
            data = dict(data)
            data['sphere'] = await InfoGet.get_sphere_id_by_subsphere_id(data['select_subsphere'])
            community_id = await CommunityCreate.create_community(user_id=user_id, data=data)
            keys = [i for i in data.keys()]
            keys_conditions = keys[keys.index('select_condition0'): keys.index('background_color1') + 1]
            data_new = {'condition_id': [], 'task': [], 'answers': [], 'condition_value': [], 'images': []}
            for i in keys_conditions:
                if 'select_condition' in i:
                    data_new['condition_id'] += [data[i]]
                    print(data[i])
                if 'task' in i:
                    if data[i] == '':
                        data_new['task'] += ['null']
                    else:
                        data_new['task'] += [data[i]]
                if 'answers' in i:
                    if data[i] == '':
                        data_new['answers'] += ['null']
                    else:
                        data_new['answers'] += [data[i]]
                if 'condition_value' in i:
                    if data[i] == '':
                        data_new['condition_value'] += ['null']
                    else:
                        data_new['condition_value'] += [data[i]]
                if 'text_color' in i:
                    if data[i] != '#000000':
                        num = i.replace('text_color', '')
                        back = 'background_color' + num
                        img = Image.new('RGB', (100, 30), color=data[back])
                        text = 'task' + num
                        d = ImageDraw.Draw(img)
                        d.text((10, 10), data[text], fill=data[i])
                        path = f'static/conditions/condition_community_{community_id}{data[text]}.png'
                        img.save(path)
                        data_new['images'] += [path.replace('static/conditions/', '')]
                    else:
                        data_new['images'] += ['null']
            await CommunityCreate.create_community_info_conditions(community_id=community_id, data=data_new)
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
        goals = await Goals.get_goals(user_id=community_id, user_type=1)
        payment_goals = await CommunityWalletGoal.get_payment_goal(community_id=community_id)
        wallets = await Wallet.get_wallet(community_id=community_id)
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
        return dict(community=community, access=access, in_community=is_in_community, subscribers=subscribers, participants=participants, participants_for_remove=participants_for_remove,
                    goals=goals, payment_goals=payment_goals, wallets=wallets)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        data = await self.post()
        user_id = self.session['user']['id']
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
            status = [1 for i in range(len(users))]
            community = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/community/')[-1][:-2]
            await CommunityAvatarAction.add_member(community_id=community, users=users, status=status)
        elif 'delete_community_member' in str(self):
            users = [int(i) for i in data.keys()]
            community = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('/community/')[-1][:-2]
            await CommunityAvatarAction.remove_member(community_id=community, users=users)
        elif 'add_payment_goal' in str(self):
            data = dict(data)
            # todo: logic for multiple responsible_users
            wallet_id = False
            # data['type'] = ''
            if data['wallet_name'] != '':
                if data['responsible_users'] != user_id:
                    data['responsible_users'] = [data['responsible_users']] + [user_id]
                wallet_id = await Wallet.create_wallet(community_id=community_id, data=data)
            if wallet_id:
                data['wallet_id'] = wallet_id
            if 'from_date' not in data.keys():
                data['from_date'] = 'null'
            if 'to_date' not in data.keys():
                data['to_date'] = 'null'
            if 'is_nessesarity' not in data.keys():
                data['is_nessesarity'] = 'false'
            if 'user_must_send' not in data.keys():
                data['user_must_send'] = 'null'
            print(data)
                # data['type'] = 'ARRAY[]::integer[]'
            await CommunityWalletGoal.create_wallet_goal(community_id=community_id, data=data)
        else:
            method = str(self).split('/')[1][:-2].split('_')[0]
            await CommunityAvatarAction.leave_join(community_id=community_id, user_id=user_id, method=method)

        return web.HTTPFound(location=location)
