import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.user import User
from models.post import Post
from models.friends import Friends


class PersonalPageView(web.View):

    @aiohttp_jinja2.template('personal_page.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()
        location = str(self).split('/')[-1][:-2]
        session = await get_session(self)
        my_page = False
        user = await User.get_user_by_id(user_id=location)
        avatar = await User.get_avatar_by_user_id(user_id=location)
        friends = await Friends.get_user_friends_names(user_id=location)
        posts = await Post.get_posts_by_user(user_id=location)
        if str(session['user']['id']) == location:
            my_page = True
        return dict(user=user, friends=friends, posts=posts, me=my_page, avatar=avatar)
