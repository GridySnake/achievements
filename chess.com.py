import requests

req = 'https://api.chess.com/pub'


def get_player_profile(username):
    request = requests.get(f'https://api.chess.com/pub/player/{username}').text
    return request


def get_player_stats(username):
    request = requests.get(f'https://api.chess.com/pub/player/{username}/stats').text
    return request


def get_player_clubs(username):
    request = requests.get(f'https://api.chess.com/pub/player/{username}/clubs').text
    return request


def get_player_tournaments(username):
    request = requests.get(f'https://api.chess.com/pub/player/{username}/tournaments').text
    return request


def get_titled_players(title_abbrev):
    request = requests.get(f'https://api.chess.com/pub/titled/{title_abbrev}').text
    return request


def get_leaderboards():
    request = requests.get(f'https://api.chess.com/pub/leaderboards').text
    return request

