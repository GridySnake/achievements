import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.user import UserGetInfo
from models.post import Post
from models.subscribes import SubscribesGetInfo
from models.achievements import AchievementsGetInfo


class PersonalPageView(web.View):

    @aiohttp_jinja2.template('personal_page.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        location = str(self).split('/user/')[-1][:-2]
        session = await get_session(self)
        my_page = False
        user = await UserGetInfo.get_user_by_id(user_id=location)
        avatar = await UserGetInfo.get_avatar_by_user_id(user_id=location)
        friends = await SubscribesGetInfo.get_user_subscribes_names(user_id=location)
        posts = await Post.get_posts_by_user(user_id=location)
        achievements_user = await AchievementsGetInfo.get_users_achievements(user_id=location)
        achievements_desired = await AchievementsGetInfo.get_users_desire_achievements(user_id=location)
        block = False
        if str(session['user']['id']) != location:
            block = await SubscribesGetInfo.is_block(user_active_id=session['user']['id'], user_passive_id=location)
        elif str(session['user']['id']) == location:
            my_page = True
        if not my_page:
            achievements_approve = await AchievementsGetInfo.get_users_approve_achievements(user_id=location, user_active=session['user']['id'])
        else:
            achievements_approve = await AchievementsGetInfo.get_users_approve_achievements(user_id=location)
        return dict(user=user, friends=friends, posts=posts, me=my_page, avatar=avatar, block=block, achievements_user=achievements_user, achievements_approve=achievements_approve, achievements_desired=achievements_desired)
