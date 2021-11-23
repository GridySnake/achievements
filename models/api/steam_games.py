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
    def get_user_info(steam_id):
        return requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={BaseConfig.steam_api_key}&steamids={steam_id}').json()['response']['players'][0]

    @staticmethod
    def get_friends(steam_id):
        return [i['steam_id'] for i in requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={BaseConfig.steam_api_key}&steamid={steam_id}&relationship=friend').json()['friendslist']['friends']]

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

    @staticmethod
    def get_achievements_of_game(steam_id, app_id):
        return [i['apiname'] for i in requests.get(f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={BaseConfig.steam_api_key}&steamid={steam_id}').json()['playerstats']['achievements']]

    @staticmethod
    def get_game_stats(steam_id, app_id):
        return {i['name']: i['value'] for i in requests.get(f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={app_id}&key={BaseConfig.steam_api_key}&steamid={steam_id}').json()['playerstats']['stats']}

    @staticmethod
    def get_games(steam_id):
        response = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={BaseConfig.steam_api_key}&steamid={steam_id}').json()['response']
        game_count = response['game_count']
        games_id_playtime = {i['appid']: i['playtime_forever'] for i in response['games']}
        return game_count, games_id_playtime

    @staticmethod
    def get_recently_played_games(steam_id):
        response = requests.get(f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={BaseConfig.steam_api_key}&steamid={steam_id}').json()['response']
        game_count = response['total_count']
        games_id_name_pt2weeks_ptforever = {i['appid']: [i['name'], i['playtime_2weeks'], i['playtime_forever']] for i in response['games']}
        return game_count, games_id_name_pt2weeks_ptforever


# userr = Steam.login('alex1212121999', '12041999alex')
# print(userr)
# print(Steam.get_user_info(SteamID(117877571)))
# print(Steam.get_user_info(117877571))
# print(Steam.get_game_stats(userr['steam_id'], 570))
# print(Steam.get_achievements_of_game(SteamID(117877571), 730))
# print(Steam.get_game_stats(userr['steam_id'], 812140))
# print(Steam.get_game_stats(userr['steam_id'], 48700))
# print(requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={BaseConfig.steam_api_key}&steamids={117877571}').json())