import twitch
from config.common import BaseConfig
helix = twitch.Helix(BaseConfig.twitch_client_id, BaseConfig.twitch_client_secret)


class Twitch:
    @staticmethod
    def get_user_info(username):
        return helix.user(username).data

    @staticmethod
    def get_user_video_info(username):
        return [video.data for video in helix.user(username).videos()]

    @staticmethod
    def get_user_followers_names(username):
        return [follower.from_name for follower in helix.user(username).following()]

    @staticmethod
    def get_user_followers_data(username):
        return [follower.data for follower in helix.user(username).following()]

    @staticmethod
    def get_user_following_names(username):
        return [following.from_name for following in helix.user(username).following()]

    @staticmethod
    def get_user_following_data(username):
        return [following.data for following in helix.user(username).following()]

    @staticmethod
    def is_online(username):
        return helix.user(username).is_live

    @staticmethod
    def get_top_games():
        return [i.data for i in helix.top_games()]

    @staticmethod
    def get_top_games_names():
        return [i.name for i in helix.top_games()]

    @staticmethod
    def get_streams():
        return [i.data for i in helix.streams()]

    @staticmethod
    def get_streams_names():
        return [i.data for i in helix.streams()]

#print(Twitch.get_user_info('crazyme1917')) #view_count, created_at