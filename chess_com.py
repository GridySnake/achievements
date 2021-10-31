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


# print(Chesscom.get_player_stats('crazyniga1917')['chess_rapid']['last'])
