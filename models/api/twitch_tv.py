import twitch
from config.common import BaseConfig
import inspect
helix = twitch.Helix(BaseConfig.twitch_client_id, BaseConfig.twitch_client_secret)


class Twitch:
    @staticmethod
    def get_user_info(username, views=False, created_at=False, broadcaster_type=False):
        frame = inspect.currentframe()
        parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
                     and i != 'views']
        data = {}
        user_data = helix.user(username).data
        if parameter:
            for j in parameter:
                data[j] = user_data[j]
        if views:
            data['views'] = user_data['view_count']
        return data

    @staticmethod
    def get_user_videos_info(username, views=False, type=False, duration=False, created_at=False):
        frame = inspect.currentframe()
        parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
                     and i != 'views']
        data = {str('video_' + i): [] for i in parameter}
        if views:
            data['video_views'] = []
        video_data = [i.data for i in helix.user(username).videos()]
        for i in video_data:
            if parameter:
                for j in parameter:
                    try:
                        data[str('video_' + j)].append(i[j])
                    except:
                        print(f'error: {i, j}')
            if views:
                data['video_views'].append(i['view_count'])
        return data

    # @staticmethod
    # def get_user_followers_data(username):
    #     frame = inspect.currentframe()
    #     parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
    #                  and i != '']
    #     data = {}
    #     if parameter:
    #
    #     return [follower.data for follower in helix.user(username).followers()]

    @staticmethod
    def get_user_following_info(username, followings=False, follow_user=None, followed_at=False):
        data = {}
        if follow_user:
            following_data = [following.data for following in helix.user(username).following()]
            if follow_user in [i['to_name'] for i in following_data]:
                data['follow_user'] = True
                if followed_at:
                    data['followed_at'] = [i['followed_at'] for i in following_data if i['to_name'] == follow_user][0]
            else:
                data['follow_user'] = False
            if followings:
                data['followings'] = len(following_data)
        elif followings:
            data['followings'] = len([following for following in helix.user(username).following()])
        return data

    # @staticmethod
    # def is_online(username):
    #     return helix.user(username).is_live

    # @staticmethod
    # def get_top_games():
    #     return [i.data for i in helix.top_games()]

    # @staticmethod
    # def get_top_games_names():
    #     return [i.name for i in helix.top_games()]

    # @staticmethod
    # def get_streams():
    #     return [i.data for i in helix.streams()]

    # @staticmethod
    # def get_streams_names():
    #     return [i.data for i in helix.streams()]

# print(Twitch.get_streams())