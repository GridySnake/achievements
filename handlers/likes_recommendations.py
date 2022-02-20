import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.likes_recommendations import LikesRecommendationsAction


class LikesRecommendationsView:

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        data = await self.post()
        if data:
            data = dict(data)
        else:
            user_type = 0
            session = await get_session(self)
            user_id = session['user']['id']
        owner = {'user': ['users_information', 'user_id', 0], 'community': ['communities', 'community_id', 1],
                 'course': ['courses', 'course_id', 2], 'achievement': ['achievements', 'achievement_id', 3]}
        location = str(self).split('/')[-1][:-2]
        like_recommend_dict = {'like': ['likes', 'liked'], 'recommend': ['recommendations', 'recommend'], 'dislike':
                               ['dislikes', 'disliked']}
        like_recommend = like_recommend_dict[location.replace('un', '')]
        for i in owner.keys():
            if i in str(self.__dict__['_message']).split('Referer')[-1].split(',')[1]:
                owner_type = owner[i]
                owner_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split(f'{i}/')[-1][:-2]
                break
        # print(like_recommend)
        # print(f"""update {like_recommend[0]}
        #                        set users_{like_recommend[1]}_id =
        #                                 array_append(users_{like_recommend[1]}_id, {user_id}),
        #                             users_{like_recommend[1]}_type =
        #                                 array_append(users_{like_recommend[1]}_type, {user_type}),
        #                             action_datetime = array_append(action_datetime, statement_timestamp())
        #                         where owner_id = {owner_id} and owner_type = {owner_id[2]}
        #                     """)
        if 'un' in location:
            await LikesRecommendationsAction.unlike_unrecommend(user_id=user_id, user_type=user_type, owner_id=owner_id,
                                                                owner_type=owner_type,
                                                                like_recommendations=like_recommend)
        else:
            await LikesRecommendationsAction.like_recommend(user_id=user_id, user_type=user_type, owner_id=owner_id,
                                                            owner_type=owner_type, like_recommendations=like_recommend)
        return web.HTTPFound(location=f"{owner_type[1].replace('_id', '')}/{owner_id}")