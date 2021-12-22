from handlers.base import Login, Signup, Logout, Verify, NeedVerify
from handlers.posts import PostView
from handlers.avatar import Avatar
from handlers.subscribes import SubscribesView, MySubscribesView
from handlers.messages import MessageView
from handlers.achievements import AchievementsView, AchievementsVerificationView, AchievementInfoView, AchievementDesireView
from handlers.communities import CommunitiesView, CommunitiesInfoView
from handlers.personal_page import PersonalPageView
from handlers.chat import ChatView
from handlers.user_info import UserInfoView
from config.common import BaseConfig
from sqlalchemy import create_engine
from aiohttp_swagger import *
#todo: изменить ссылки на страницы, а то из подтврждения ачивок не падаем на нужные страницы
engine = create_engine(BaseConfig.database_url)

len_users = len(engine.execute(f"""
select user_id
from users_main
""").fetchall())

verify = [str(i[0]) for i in engine.execute(f"""
select verifying_token
from authentication
where verifying_token is not null
""").fetchall()]

verify_achievement_qr = [str(i[0]) for i in engine.execute(f"""
select value
from achi_conditions
where achi_condition_group_id = 1
""").fetchall()]

verify_achievement_location = [str(i[0]) for i in engine.execute(f"""
select condition_id
from achi_conditions
where achi_condition_group_id = 2
""").fetchall()]

verify_achievement_service = [str(i[0]) for i in engine.execute(f"""
select parameter
from achi_conditions
where achi_condition_group_id = 3
""").fetchall()]

achievements = [str(i[0]) for i in engine.execute(f"""
select achievement_id 
from achievements
""").fetchall()]

communities = [str(i).split(',')[0][1:] for i in engine.execute(f"""
select community_id 
from communities
""").fetchall()]


def setup_routes(app):
    app.router.add_route('GET', '/login', Login.get, name='login')
    app.router.add_route('POST', '/login', Login.post)
    app.router.add_route('GET', '/signup', Signup.get, name='signup')
    app.router.add_route('POST', '/signup', Signup.post)
    app.router.add_route('GET', '/logout', Logout.get, name='logout')
    app.router.add_route('POST', '/save_avatar', Avatar.post, name='save_avatar')
    app.router.add_route('POST', '/add_post', PostView.post, name='add_post')
    app.router.add_route('GET', '/subscribes', SubscribesView.get, name='subscribes')
    app.router.add_route('POST', '/subscribe', SubscribesView.post, name='subscribe')
    app.router.add_route('GET', '/messages', MessageView.get, name='messages')
    app.router.add_route('POST', '/send_message', MessageView.post, name='send_message')
    app.router.add_route('GET', '/my_subscribes', MySubscribesView.get, name='my_subscribes')
    app.router.add_route('GET', '/achievements', AchievementsView.get, name='achievements')
    app.router.add_route('POST', '/add_achievement', AchievementsView.post, name='add_achievement')
    app.router.add_route('POST', '/user_info', UserInfoView.post, name='user_info')
    app.router.add_route('GET', '/user_info', UserInfoView.get, name='user_info')
    app.router.add_route('GET', '/verify', NeedVerify.get, name='verify')
    app.router.add_route('POST', '/my_subscribes', MySubscribesView.post, name='matching_follow')
    app.router.add_route('POST', '/verify_message_to_achi', AchievementInfoView.post, name='verify_message_to_achi')
    app.router.add_route('POST', '/desire', AchievementDesireView.post, name='desire')
    app.router.add_route('POST', '/approve', AchievementDesireView.post, name='approve')
    app.router.add_route('GET', '/community', CommunitiesView.get, name='community')
    app.router.add_route('POST', '/create_community', CommunitiesView.post, name='create_community')
    app.router.add_route('POST', '/save_community_avatar', CommunitiesInfoView.post, name='save_community_avatar')
    app.router.add_route('POST', '/leave_community', CommunitiesInfoView.post, name='leave_community')
    app.router.add_route('POST', '/join_community', CommunitiesInfoView.post, name='join_community')
    app.router.add_route('GET', '/posts', PostView.get, name='posts')
    app.router.add_route('GET', '/my_posts', PostView.get, name='my_posts')

    for i in range(len_users):
        app.router.add_route('GET', f'/{i}', PersonalPageView.get, name=f'personal_page_{i}')
        app.router.add_route('GET', f'/chat_{i}', ChatView.get, name=f'chat_{i}')
    for i in verify:
        app.router.add_route('GET', f'/verify/{i}', Verify.get, name=f'verify_{i}')
    for i in verify_achievement_qr:
        app.router.add_route('GET', f'/verify_achievement/qr/{i}', AchievementsVerificationView.get, name=f'verify_achievement_qr_{i}')
    for i in achievements:
        app.router.add_route('GET', f'/achievement/{i}', AchievementInfoView.get, name=f'achievement_{i}')
    for i in verify_achievement_location:
        app.router.add_route('GET', f'/verify_achievement/location/{i}', AchievementsVerificationView.get, name=f'verify_achievement_location_{i}')
    for i in verify_achievement_service:
        app.router.add_route('GET', f'/verify_achievement/service/{i}', AchievementsVerificationView.get, name=f'verify_achievement_service_{i}')
    for i in communities:
        app.router.add_route('GET', f'/community/{i}', CommunitiesInfoView.get, name=f'community_{i}')
    setup_swagger(app)


def setup_static_routes(app):
    app.router.add_static('/static/', path=BaseConfig.STATIC_DIR, name='static')
