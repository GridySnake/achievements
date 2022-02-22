import json

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.user import UserGetInfo
from models.post import Post
from models.subscribes import SubscribesGetInfo
from models.achievements import AchievementsGetInfo
from models.conditions import ConditionsGetInfo
from models.likes_recommendations import LikesRecommendationsGetInfo
from aiohttp.web import json_response


class PersonalPageView(web.View):

    # @aiohttp_jinja2.template('personal_page.html')
    async def get(self):
        # if 'user' not in self.session:
        #     return web.HTTPFound(location=self.app.router['login'].url_for())

        location = str(self).split('/user/')[-1][:-2]
        print(location)
        # session = await get_session(self)
        my_page = False
        user = await UserGetInfo.get_user_by_id(user_id=location)
        # avatar = await UserGetInfo.get_avatar_by_user_id(user_id=location)
        friends = await SubscribesGetInfo.get_user_subscribes_names(user_id=location)
        posts = await Post.get_posts_by_user(user_id=location)
        achievements_user = await AchievementsGetInfo.get_users_achievements(user_id=location)
        achievements_desired = await AchievementsGetInfo.get_users_desire_achievements(user_id=location)
        block = False
        condition_to_chat = False
        allow = True
        user_id = location#str(session['user']['id'])
        if user_id == location:
            like = False
            recommend = False
            dislike = False
            my_page = True
        if not my_page:
            friend = await SubscribesGetInfo.subscribe_each_other(user_active_id=user_id,
                                                                  user_passive_id=location)
            achievements_approve = await AchievementsGetInfo.get_users_approve_achievements(user_id=location,
                                                                                            user_active=user_id)
            like, recommend, dislike = await LikesRecommendationsGetInfo.is_like_recommend(user_id=user_id, user_type=0,
                                                                                  owner_id=location, owner_type=0)
            if not friend:
                block = await SubscribesGetInfo.is_block(user_active_id=user_id, user_passive_id=location)
                if not block:
                    can_chat = await ConditionsGetInfo.is_allowed_communicate_by_conditions(user_active_id=user_id,
                                                                                            user_passive_id=location,
                                                                                            owner_table=
                                                                                            'users_information',
                                                                                            owner_column='user_id')
                    if not can_chat:
                        condition_to_chat = await UserGetInfo.get_user_conditions(user_active_id=user_id,
                                                                                  user_passive_id=location)
                        allow = False
        else:
            achievements_approve = await AchievementsGetInfo.get_users_approve_achievements(user_id=location)
        values = [dict(record) for record in friends]
        friends = json.dumps(values).replace("</", "<\\/")
        print(friends)
        # friends = json.dumps(friends)
        return json_response(friends)
        # posts=posts, me=my_page, block=block, recommend=recommend,
        #             achievements_user=achievements_user, achievements_approve=achievements_approve, like=like,
        #             achievements_desired=achievements_desired, condition_to_chat=condition_to_chat, allow=allow,
        #             dislike=dislike)
