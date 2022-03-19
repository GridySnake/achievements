from models.likes_recommendations import LikesRecommendationsAction, LikesRecommendationsGetInfo
import json
from aiohttp.web import json_response


async def likes_recommendations(request):
    pool = request.app['pool']
    data = await request.json()
    user_type = 0
    user_id = json.loads(request.cookies['user'])['user_id']
    owner = {'user': ['users_information', 'user_id', 0], 'community': ['communities', 'community_id', 1],
             'course': ['courses', 'course_id', 2], 'achievement': ['achievements', 'achievement_id', 3]}
    location = str(request).split('/')[-1][:-2]
    like_recommend_dict = {'like': ['likes', 'liked'], 'recommend': ['recommendations', 'recommend'], 'dislike':
                           ['dislikes', 'disliked']}
    like_recommend = like_recommend_dict[location.replace('un', '')]
    owner_type = owner[data['owner_type']]
    owner_id = data['owner_id']
    owner_type_new = {0: 'user', 1: 'community', 2: 'course', 3: 'achievement'}
    async with pool.acquire() as conn:
        if 'un' in location:
            await LikesRecommendationsAction.unlike_unrecommend(user_id=user_id, user_type=user_type, owner_id=owner_id,
                                                                owner_type=owner_type,
                                                                like_recommendations=like_recommend, conn=conn)
        else:
            await LikesRecommendationsAction.like_recommend(user_id=user_id, user_type=user_type, owner_id=owner_id,
                                                            owner_type=owner_type, like_recommendations=like_recommend,
                                                            conn=conn)
        value = await LikesRecommendationsGetInfo.get_one_statistic(owner_id=user_id,
                                                                    owner_type=owner_type_new[owner_type],
                                                                    statistic=like_recommend[0], conn=conn)

    return json_response({'value': value})
