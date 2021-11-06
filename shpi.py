import twitch
from config.common import BaseConfig
helix = twitch.Helix(BaseConfig.twitch_client_id, BaseConfig.twitch_client_secret)

from TikTokApi import TikTokApi
api = TikTokApi()

# results = 5
# trending = api.by_trending(count=results)
# for tiktok in trending:
#     print(tiktok)
# print(len(trending))
# print(api.by_username('mfsisthat'))
# print(api.get_user('mfsisthat'))
#print()

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
#print([i for i in helix.video(350637800).comments])

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
