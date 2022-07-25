from handlers.base import *
from handlers.posts import *
from handlers.avatar import *
from handlers.subscribes import *
from handlers.messages import *
from handlers.achievements import *
from handlers.communities import *
from handlers.courses import *
from handlers.personal_page import personal_page
from handlers.chat import get_chat
from handlers.user_info import *
from handlers.goal import GoalView
from handlers.conditions import *
from handlers.likes_recommendations import likes_recommendations
from aiohttp_swagger import *
#todo: изменить ссылки на страницы, а то из подтврждения ачивок не падаем на нужные страницы


def setup_routes(app):
    app.router.add_route('POST', '/login', login)
    app.router.add_route('GET', '/signup', Signup.get, name='signup')
    app.router.add_route('POST', '/signup', Signup.post)
    app.router.add_route('GET', '/logout', Logout.get, name='logout')
    app.router.add_route('POST', '/save_avatar', Avatar.post, name='save_avatar')
    app.router.add_route('POST', '/add_post', PostView.post, name='add_post')
    app.router.add_route('GET', '/subscribes', get_subscribes, name='subscribes')
    app.router.add_route('GET', '/subscribes_suggestions', get_subscribes_suggestions, name='get_subscribes_suggestions')
    app.router.add_route('POST', '/subscribe', SubscribesView.post, name='subscribe')
    app.router.add_route('GET', '/messages', messages, name='messages')
    app.router.add_route('POST', '/send_message', send_message, name='send_message')
    app.router.add_route('GET', '/my_subscribes', MySubscribesView.get, name='my_subscribes')
    app.router.add_route('GET', '/achievements', get_achievements, name='achievements')
    app.router.add_route('POST', '/add_achievement', create_achievement, name='add_achievement')
    app.router.add_route('POST', '/user_info', change_user_info, name='user_info')
    app.router.add_route('GET', '/user_info', get_user_info, name='user_info')
    app.router.add_route('GET', r'/get_cities_by_country/{i}', get_cities_by_country, name='get_cities_by_country')
    app.router.add_route('GET', r'/get_subspheres_by_sphere/{i}', get_subspheres_by_sphere,
                         name='get_subspheres_by_sphere')
    app.router.add_route('GET', r'/get_conditions_by_group/{i}', get_conditions_by_group,
                         name='get_conditions_by_group')
    app.router.add_route('GET', r'/get_conditions_by_service/{i}', get_conditions_by_service,
                         name='get_conditions_by_service')
    app.router.add_route('GET', r'/get_conditions_by_aggregation/{i}', get_conditions_by_agg_group,
                         name='get_conditions_by_aggregation')
    app.router.add_route('GET', r'/get_users_by_type/{i}', get_users_by_type,
                         name='get_users_by_type')
    app.router.add_route('GET', '/verify', NeedVerify.get, name='verify')
    app.router.add_route('POST', '/unfollow', unfollow, name='unfollow')
    app.router.add_route('POST', '/follow', follow, name='follow')
    app.router.add_route('POST', '/block', block, name='block')
    app.router.add_route('POST', '/unblock', unblock, name='unblock')
    app.router.add_route('POST', '/verify_message_to_achi', AchievementInfoView.post, name='verify_message_to_achi')
    app.router.add_route('POST', '/desire', desire_achievement, name='desire')
    app.router.add_route('POST', '/drop_achievement', drop_achievement, name='drop_achievement')
    app.router.add_route('POST', '/show_achievement', show_achievement, name='show_achievement')
    app.router.add_route('POST', '/hide_achievement', hide_achievement, name='hide_achievement')
    app.router.add_route('POST', '/approve', AchievementDesireView.post, name='approve')
    app.router.add_route('GET', '/community', CommunitiesView.get, name='community')
    app.router.add_route('POST', '/create_community', CommunitiesView.post, name='create_community')
    app.router.add_route('POST', '/save_community_avatar', CommunitiesInfoView.post, name='save_community_avatar')
    app.router.add_route('POST', '/leave_community', CommunitiesInfoView.post, name='leave_community')
    app.router.add_route('POST', '/join_community', CommunitiesInfoView.post, name='join_community')
    app.router.add_route('GET', '/posts', PostView.get, name='posts')
    app.router.add_route('GET', '/my_posts', PostView.get, name='my_posts')
    app.router.add_route('GET', '/goals', GoalView.get, name='goals')
    app.router.add_route('POST', '/add_content', CourseContentCreate.post, name='add_content')
    app.router.add_route('POST', '/add_chat_member', add_chat_member, name='add_chat_member')
    app.router.add_route('POST', '/remove_chat_member', remove_chat_member, name='remove_chat_member')
    app.router.add_route('POST', '/create_group_chat', create_group_chat, name='create_group_chat')
    app.router.add_route('POST', '/create_user_chat', create_user_chat, name='create_user_chat')
    app.router.add_route('POST', '/add_community_member', CommunitiesInfoView.post, name='add_community_member')
    app.router.add_route('POST', '/remove_community_member', CommunitiesInfoView.post, name='remove_community_member')
    app.router.add_route('GET', '/courses', get_courses, name='courses')
    app.router.add_route('GET', r'/chat/{i}', get_chat, name='chat')
    app.router.add_route('GET', r'/verify/{i}', Verify.get, name='verify_i')
    app.router.add_route('POST', r'/verify_achievement', AchievementsVerificationView.post, name='verify_achievement')
    app.router.add_route('POST', r'/verify_achievement/{i}', AchievementsVerificationView.post,
                         name='qr_verify_achievement')
    app.router.add_route('GET', r'/achievement/{i}', get_achievement_info, name='achievement')
    app.router.add_route('GET', r'/community/{i}', CommunitiesInfoView.get, name='community_info')
    app.router.add_route('GET', r'/community/{i}/cover_letter_interview', ApproveConditionsView.get,
                         name='cover_letter_interview_community')
    app.router.add_route('POST', '/course_action', CourseInfoView.post, name='course_action')
    app.router.add_route('POST', '/create_course', CoursesView.post, name='create_course')
    app.router.add_route('GET', r'/course/{i}', get_course_info, name='course')
    app.router.add_route('GET', r'/course/{i}/cover_letter_interview', ApproveConditionsView.get,
                         name='cover_letter_interview_course')
    app.router.add_route('GET', r'/course/{i}/course_content/{j}', CourseContent.get, name='course_content')
    app.router.add_route('GET', r'/create_course_content/{i}', CourseContentCreate.get, name='create_course_content')
    app.router.add_route('POST', r'/accept_invitation_community/{i}', CommunitiesView.post,
                         name='accept_invitation_community')
    app.router.add_route('POST', r'/decline_invitation_community/{i}', CommunitiesView.post,
                         name='decline_invitation_community')
    app.router.add_route('POST', r'/accept_invitation_course/{i}', CoursesView.post, name='accept_invitation_course')
    app.router.add_route('POST', r'/decline_invitation_course/{i}', CoursesView.post, name='decline_invitation_course')
    app.router.add_route('POST', '/add_course_member', CourseInfoView.post, name='add_course_member')
    app.router.add_route('POST', '/remove_course_member', CourseInfoView.post, name='remove_course_member')
    app.router.add_route('POST', '/add_payment_goal', CommunitiesInfoView.post, name='add_payment_goal')
    app.router.add_route('POST', '/approve_conditions', ApproveConditionsView.post, name='approve_conditions')
    app.router.add_route('POST', '/like', likes_recommendations, name='like')
    app.router.add_route('POST', '/unlike', likes_recommendations, name='unlike')
    app.router.add_route('POST', '/dislike', likes_recommendations, name='dislike')
    app.router.add_route('POST', '/undislike', likes_recommendations, name='undislike')
    app.router.add_route('POST', '/recommend', likes_recommendations, name='recommend')
    app.router.add_route('POST', '/unrecommend', likes_recommendations, name='unrecommend')
    app.router.add_route('POST', '/accept_cl', ApproveConditionsView.post, name='accept_cl')
    app.router.add_route('POST', '/decline_cl', ApproveConditionsView.post, name='decline_cl')
    app.router.add_route('POST', '/update_interview', ApproveConditionsView.post, name='update_interview')
    app.router.add_route('POST', '/accept_int', ApproveConditionsView.post, name='accept_int')
    app.router.add_route('POST', '/decline_int', ApproveConditionsView.post, name='decline_int')
    app.router.add_route('GET', r'/user/{i}', personal_page, name='personal_page')
    app.router.add_route('GET', r'/user/{i}/cover_letter_interview', ApproveConditionsView.get,
                         name='cover_letter_interview_user')
    app.router.add_route('GET', '/communities', communities_page, name='communities_page')
    app.router.add_route('GET', '/auth', auth)
    app.router.add_route('POST', '/upload_group_avatar', upload)

    setup_swagger(app)


def setup_static_routes(app):
    app.router.add_static('/static/', path=BaseConfig.STATIC_DIR, name='static')

