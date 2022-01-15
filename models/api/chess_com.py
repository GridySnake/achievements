import pandas as pd
import requests


class Chesscom:

    @staticmethod
    def get_player_profile(username):
        request = requests.get(f'https://api.chess.com/pub/player/{username}').json()
        return request

    @staticmethod
    def get_player_stats(username):
        request = requests.get(f'https://api.chess.com/pub/player/{username}/stats').json()
        return request

    @staticmethod
    def get_player_clubs(username):
        request = requests.get(f'https://api.chess.com/pub/player/{username}/clubs').json()
        return request

    @staticmethod
    def get_player_tournaments(username):
        request = requests.get(f'https://api.chess.com/pub/player/{username}/tournaments').json()
        return request

    @staticmethod
    def get_titled_players(title_abbrev):
        request = requests.get(f'https://api.chess.com/pub/titled/{title_abbrev}').json()
        return request

    @staticmethod
    def get_leaderboards():
        request = requests.get(f'https://api.chess.com/pub/leaderboards').json()
        return request

# print(Chesscom.get_player_stats('crazyniga1917'))
# d = Chesscom.get_player_stats('crazyniga1917') #player_id, followers, joined, status, is_streamer
# # a=[]
# print('get_player_stats')
# for k,v in d.items():
#     print(k,v)

# d = Chesscom.get_player_profile('crazyniga1917')
# print('get_player_profile')
# print(d)
# for i in d:
#     for k,v in d.items():
#         if k != 'fide':
#             for l, s in v.items():
#                 if l == 'last':
#                     for m,n in s.items():
#                         if m == 'date':
#                             a.append(n)
# print(pd.Timestamp(a[0]))