import json
from models.user import UserGetInfo
from models.post import Post
from models.subscribes import SubscribesGetInfo
from models.achievements import AchievementsGetInfo
from models.conditions import ConditionsGetInfo
from models.likes_recommendations import LikesRecommendationsGetInfo
from aiohttp.web import json_response


async def personal_page(request):
    location = str(request).split('/user/')[-1][:-2]
    my_page = False
    user = await UserGetInfo.get_user_by_id(user_id=location)
    subscribes = await SubscribesGetInfo.get_user_subscribes_names(user_id=location)
    posts = await Post.get_posts_by_user(user_id=location)
    achievements = await AchievementsGetInfo.get_users_achievements(user_id=location)
    goals = await AchievementsGetInfo.get_users_desire_achievements(user_id=location)
    user_id = json.loads(request.cookies['user'])['user_id']
    statistics = await LikesRecommendationsGetInfo.get_statistics(owner_id=location, owner_type='user')
    condition_to_chat = None
    allow = None
    actions = None
    block = None
    if user_id == location:
        my_page = True
        approve = await AchievementsGetInfo.get_users_approve_achievements(user_id=location)
    else:
        friend = await SubscribesGetInfo.subscribe_each_other(user_active_id=user_id,
                                                              user_passive_id=location)
        approve = await AchievementsGetInfo.get_users_approve_achievements(user_id=location, user_active=user_id)
        actions = await LikesRecommendationsGetInfo.is_like_recommend(user_id=user_id, user_type=0, owner_id=location,
                                                                      owner_type=0)
        allow = True
        block = False
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
            else:
                block = True
    return json_response({'user': user, 'statistics': statistics, 'posts': posts, 'myPage': my_page,
                          'subscribes': subscribes, 'achievements': achievements, 'goals': goals,
                          'conditions': condition_to_chat, 'allow': allow, 'block': block, 'actions': actions,
                          'approve': approve})
