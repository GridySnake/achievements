from handlers.base import Login, Signup, Logout, Verify, NeedVerify
from handlers.posts import PostView
from handlers.avatar import Avatar
from handlers.friends import FriendsView, MyFriendsView
from handlers.messages import MessageView
from handlers.achievements import AchievementsView, AchievementsVerificationView, AchievementInfoView, AchievementDesireView
from handlers.communities import CommunitiesView
from handlers.personal_page import PersonalPageView
from handlers.chat import ChatView
from handlers.user_info import UserInfoView
from config.common import BaseConfig
from sqlalchemy import create_engine
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


def setup_routes(app):
    app.router.add_get('/login', Login.get, name='login')
    app.router.add_post('/login', Login.post)
    app.router.add_get('/signup', Signup.get, name='signup')
    app.router.add_post('/signup', Signup.post)
    app.router.add_get('/logout', Logout.get, name='logout')
    app.router.add_post('/save_avatar', Avatar.post, name='save_avatar')
    app.router.add_post('/add_post', PostView.post, name='add_post')
    app.router.add_get('/friends', FriendsView.get, name='friends')
    app.router.add_post('/add_friend', FriendsView.post, name='add_friend')
    app.router.add_get('/messages', MessageView.get, name='messages')
    app.router.add_post('/send_message', MessageView.post, name='send_message')
    app.router.add_get('/my_friends', MyFriendsView.get, name='my_friends')
    app.router.add_get('/achievements', AchievementsView.get, name='achievements')
    app.router.add_post('/add_achievement', AchievementsView.post, name='add_achievement')
    app.router.add_post('/user_info', UserInfoView.post, name='user_info')
    app.router.add_get('/user_info', UserInfoView.get, name='user_info')
    app.router.add_get('/verify', NeedVerify.get, name='verify')
    app.router.add_post('/my_friends', MyFriendsView.post, name='confirm_friend')
    app.router.add_post('/verify_message_to_achi', AchievementInfoView.post, name='verify_message_to_achi')
    app.router.add_post('/desire', AchievementDesireView.post, name='desire')
    app.router.add_post('/approve', AchievementDesireView.post, name='approve')
    app.router.add_get('/community', CommunitiesView.get, name='community')
    app.router.add_post('/create_community', CommunitiesView.post, name='create_community')
    for i in range(len_users):
        app.router.add_get(f'/{i}', PersonalPageView.get, name=f'personal_page_{i}')
        app.router.add_get(f'/chat_{i}', ChatView.get, name=f'chat_{i}')
    for i in verify:
        app.router.add_get(f'/verify/{i}', Verify.get, name=f'verify_{i}')
    for i in verify_achievement_qr:
        app.router.add_get(f'/verify_achievement/qr/{i}', AchievementsVerificationView.get, name=f'verify_achievement_qr_{i}')
    for i in achievements:
        app.router.add_get(f'/achievement/{i}', AchievementInfoView.get, name=f'achievement_{i}')
    for i in verify_achievement_location:
        app.router.add_get(f'/verify_achievement/location/{i}', AchievementsVerificationView.get, name=f'verify_achievement_location_{i}')
    for i in verify_achievement_service:
        app.router.add_get(f'/verify_achievement/service/{i}', AchievementsVerificationView.get, name=f'verify_achievement_service_{i}')


def setup_static_routes(app):
    app.router.add_static('/static/', path=BaseConfig.STATIC_DIR, name='static')
