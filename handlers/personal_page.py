import json

from handlers.achievements import verify_achievement
from models.user import UserGetInfo
from models.post import Post
from models.subscribes import SubscribesGetInfo
from models.achievements import AchievementsGetInfo
from models.conditions import ConditionsGetInfo
from models.likes_recommendations import LikesRecommendationsGetInfo
from aiohttp.web import json_response
from models.achievements import AchievementsGiveVerify, AchievementsDesireApprove
from aiohttp import web


async def personal_page(request):
    pool = request.app['pool']
    location = str(request).split('/user/')[-1][:-2]
    my_page = False
    condition_to_chat = None
    allow = None
    actions = [True, True, True]
    block = None
    need_verify = None
    user_id = json.loads(request.cookies['user'])['user_id']
    async with pool.acquire() as conn:
        user = await UserGetInfo.get_user_by_id(user_id=location, conn=conn)
        subscribes = await SubscribesGetInfo.get_user_subscribes_names(user_id=location, conn=conn)
        posts = await Post.get_posts_by_user(user_id=location, conn=conn)
        achievements = await AchievementsGetInfo.get_users_achievements(user_id=location, conn=conn)
        goals = await AchievementsGetInfo.get_users_desire_achievements(user_id=location, conn=conn)
        statistics = await LikesRecommendationsGetInfo.get_statistics(owner_id=location, owner_type='user', conn=conn)
        approve = await AchievementsGetInfo.get_users_approve_achievements(user_id=location,
                                                                           parameter='achievements_desired_id',
                                                                           conn=conn)
        approve_got = await AchievementsGetInfo.get_users_approve_achievements(user_id=location,
                                                                               parameter='achievements_id', conn=conn)
        if user_id == location:
            my_page = True
            is_approved = None
            is_approved_got = None
        else:
            friend = await SubscribesGetInfo.subscribe_each_other(user_active_id=user_id,
                                                                  user_passive_id=location, conn=conn)
            actions = await LikesRecommendationsGetInfo.is_like_recommend(user_id=user_id, user_type=0,
                                                                          owner_id=location,
                                                                          owner_type=0, conn=conn)
            is_approved = await AchievementsGetInfo.is_user_approved(user_id=location, user_active_id=user_id,
                                                                     parameter='achievements_desired_id', conn=conn)
            is_approved_got = await AchievementsGetInfo.is_user_approved(user_id=location, user_active_id=user_id,
                                                                         parameter='achievements_id', conn=conn)
            allow = True
            block = False
            if not friend:
                block = await SubscribesGetInfo.is_block(user_active_id=user_id, user_passive_id=location, conn=conn)
                if not block:
                    can_chat = await ConditionsGetInfo.is_allowed_communicate_by_conditions(user_active_id=user_id,
                                                                                            user_passive_id=location,
                                                                                            owner_table=
                                                                                            'users_information',
                                                                                            owner_column='user_id',
                                                                                            conn=conn)
                    if not can_chat:
                        condition_to_chat = await UserGetInfo.get_user_conditions(user_active_id=user_id,
                                                                                  user_passive_id=location, conn=conn)
                else:
                    block = True
        if approve:
            verify = [i['achievement_id'] for i in approve if i['approve_count'] >= i['approve_need'] and
                      int(i['delta']) >= 5]
            if len(verify) > 0:
                need_verify = verify

            # for achievement_id in verify:
            #     conditions = await AchievementsGetInfo.get_achievement_conditions(achievement_id=achievement_id,
            #                                                                       user_id=location, conn=conn)
            #     groups = [i for i in set([i['condition_group_id'] for i in conditions]) if i != 7]
            #     if len(groups) == 0:
            #         await AchievementsGiveVerify.give_achievement_to_user(user_id=location,
            #                                                               achievement_id=achievement_id,
            #                                                               user_type=0, conn=conn)
            #         if await AchievementsDesireApprove.is_desire_achievement(user_id=location,
            #                                                                  achievement_id=achievement_id, conn=conn):
            #             await AchievementsDesireApprove.undesire_achievement(user_id=location, user_type=0,
            #                                                                  achievement_desire_id=achievement_id,
            #                                                                  conn=conn)

    return json_response({'user': user, 'statistics': statistics, 'posts': posts, 'myPage': my_page,
                          'subscribes': subscribes, 'achievements': achievements, 'goals': goals,
                          'conditions': condition_to_chat, 'allow': allow, 'block': block, 'actions': actions,
                          'approve': approve, 'is_approved': is_approved, 'need_verify': need_verify,
                          'approve_got': approve_got, 'is_approved_got': is_approved_got})
