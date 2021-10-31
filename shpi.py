import twitch
from config.common import BaseConfig


class Twitch:
    helix = twitch.Helix(BaseConfig.twitch_client_id, BaseConfig.twitch_client_secret)

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


client_id = 'blif82wvvraojfm84xp82fam1ljnii'
client_secret = 'abqm6gspq4lhaddede83szum1u0v2b'
user = 'crazyniga1917'
# helix = twitch.Helix(client_id, client_secret)
# a = helix.user('Flashynthen1ght').videos()
# print(a)
helix = twitch.Helix(client_id, client_secret)
# for user, videos in helix.users(['Flashynthen1ght']).videos():
#     print(user.display_name)
#     for i in videos:
#         print(i.data)
# for i in helix.user('Flashynthen1ght').chatters:
#     print(i)
print([i for i in helix.video(350637800).comments])

# print(helix.video(1183094159).view_count)

# profile = chessdotcom.get_player_profile(user).json['player']
# profile_current_games = chessdotcom.get_player_current_games(user)
# profile_clubs = chessdotcom.get_player_clubs(user).json
# profile_tournaments = chessdotcom.get_player_tournaments(user)
# profile_stats_modes = chessdotcom.get_player_stats(user).json['stats']
# profile_chess_rapid_last = profile_stats_modes['chess_rapid']['last']
# profile_chess_rapid_best = profile_stats_modes['chess_rapid']['best']
# profile_chess_rapid_stats = profile_stats_modes['chess_rapid']['record']
# profile_chess_blitz_last = profile_stats_modes['chess_blitz']['last']
# profile_chess_blitz_stats = profile_stats_modes['chess_blitz']['record']
# profile_fide = profile_stats_modes['fide']
# profile_tactics_highest = profile_stats_modes['tactics']['highest']
# profile_tactics_lowest = profile_stats_modes['tactics']['lowest']
# profile_lessons = profile_stats_modes['lessons']  # todo: add parameters
# profile_puzzle_rush = chessdotcom.get_player_stats(user).json['stats']['puzzle_rush']['best']
# grand_masters = chessdotcom.get_titled_players('GM').json['players']  # todo: others titles
# leaderboards = chessdotcom.get_leaderboards().json['leaderboards']['daily']  # todo: others features
#
# print(profile)

# helix = twitch.Helix(client_id, client_secret)
# us = helix.user('Flashynthen1ght').followers
# print(us)
# print(requests.get('https://api.twitch.tv/v5/videos/1191177667/comments',
#                    headers={'client-id': client_id, 'Authorization': client_secret}))

#print(hashlib.sha256('0-profile_stats_chess_rapid-last-more'.encode('utf8')).hexdigest())
