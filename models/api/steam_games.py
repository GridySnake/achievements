from config.common import BaseConfig
import requests
from steam.client import SteamClient
from steam.steamid import SteamID


class Steam:
    @staticmethod
    def login(username, password):
        client = SteamClient()
        client.cli_login(username=username, password=password)
        user = {'username': client.user.name, 'steam_id': client.steam_id, 'url': client.steam_id.community_url}
        client.logout()
        return user

    @staticmethod
    def get_user_info(steam_id, *args):
        steam_id = SteamID(steam_id)
        data = {}
        response = requests.get(
            f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={BaseConfig.steam_api_key}&steamids={steam_id}').json()[
            'response']['players'][0]
        if 'created_at' in args[0]:
            data['created_at'] = response['timecreated']
        if 'communities' in args[0]:
            data['communities'] = response['communityvisibilitystate']
        return data

    @staticmethod
    def get_friends(steam_id, *args):
        steam_id = SteamID(steam_id)
        data = {}
        response = [i for i in requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={BaseConfig.steam_api_key}&steamid={steam_id}&relationship=friend').json()['friendslist']['friends'] if i['relationship'] == 'friend']
        if 'friends' in args[0]:
            data['friends'] = len(response)
        return data

    @staticmethod
    def get_app_id_via_app_name(app_name):
        ids = {i['name']: i['appid'] for i in requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001/').json()['applist']['apps']['app']}
        try:
            app_id = ids[app_name]
        except:
            app_id = None
        return app_id

    @staticmethod
    def get_app_name_via_app_id(app_id):
        names = {i['appid']: i['name'] for i in requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001/').json()['applist']['apps']['app']}
        try:
            app_name = names[app_id]
        except:
            app_name = None
        return app_name

    # @staticmethod
    # def get_achievements_of_game(steam_id, app_id):
    #     return [i['apiname'] for i in requests.get(f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={BaseConfig.steam_api_key}&steamid={steam_id}').json()['playerstats']['achievements']]

    @staticmethod
    # todo: сделать для разных игр разные параметры
    # todo: ачивки тут
    def get_game_stats(steam_id, app_id):
        print(requests.get(f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={app_id}&key={BaseConfig.steam_api_key}&steamid={steam_id}').json())
        return {i['name']: i['value'] for i in requests.get(f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={app_id}&key={BaseConfig.steam_api_key}&steamid={steam_id}').json()['playerstats']['stats']}

    @staticmethod
    def get_games(steam_id, game_id=None, *args):#games=False, total_play_time=False, game_id=False, game_play_time=False):
        # todo: нет доты, у нее свое апи: https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1rankings%2Fget
        steam_id = SteamID(steam_id)
        response = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={BaseConfig.steam_api_key}&steamid={steam_id}').json()['response']
        data = {}
        if 'games' in args[0]:
            data['games'] = response['game_count']
        if 'total_play_time' in args[0]:
            data['total_play_time'] = sum([i['playtime_forever'] for i in response['games']])/60
        if game_id and 'game_play_time' in args[0]:
            data['game_play_time'] = [i['playtime_forever'] for i in response['games'] if i['appid'] == game_id]
        return data

    # @staticmethod
    # def get_recently_played_games(steam_id):
    #     response = requests.get(f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={BaseConfig.steam_api_key}&steamid={steam_id}').json()['response']
    #     game_count = response['total_count']
    #     games_id_name_pt2weeks_ptforever = {i['appid']: [i['name'], i['playtime_2weeks'], i['playtime_forever']] for i in response['games']}
    #     return game_count, games_id_name_pt2weeks_ptforever


max_app_id = 82103
# userr = Steam.login('alex1212121999', '12041999alex')
# print(userr)
# print(Steam.get_user_info(SteamID(117877571)))
# print(Steam.get_user_info(117877571))
# print(Steam.get_game_stats(SteamID(117877571), 730))
# print(Steam.get_game_stats(userr['steam_id'], 570))
# print(Steam.get_achievements_of_game(SteamID(117877571), 730))
# print(Steam.get_game_stats(SteamID(117877571), 812140))
# print(Steam.get_game_stats(SteamID(117877571), 48700))
# print(Steam.get_app_name_via_app_id(app_id=82103))
# print(requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={BaseConfig.steam_api_key}&steamids={117877571}').json())
#76561198068649541
# print(Steam.get_game_stats(SteamID(76561199174329979), 730))
# req = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={BaseConfig.steam_api_key}&steamid={SteamID(117877571)}').json()['response']
# print([i for i in req['games']])
# print(requests.get('https://api.opendota.com/api/players/76561198068649541/rankings').json())
# print(Steam.get_games(SteamID(76561198068649541), game_id=570))
# ddict = {}
# games = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={BaseConfig.steam_api_key}&steamid={SteamID(117877571)}').json()['response']['games']
# for i in games:
#     print(i)
#     ddict[Steam.get_app_name_via_app_id(i['appid'])] = i['playtime_forever']
# print(ddict)
import datetime
# print(datetime.datetime.fromtimestamp(Steam.get_user_info(SteamID(76561198068649541), created_at=True)['created_at']))
# steam_id = SteamID(76561199174329979)
# print(requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={BaseConfig.steam_api_key}&steamid={steam_id}&relationship=friend').json())

# print(Steam.get_games(117877571, None, ('total_play_time')))