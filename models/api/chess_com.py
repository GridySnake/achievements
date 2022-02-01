import requests
import inspect


class Chesscom:

    @staticmethod
    def get_player_profile(username, *args):#followers=False, created_at=False, status=False, streamer=False):
        parameter = [i for i in args[0]]
        request = requests.get(f'https://api.chess.com/pub/player/{username}').json()
        data = {}
        if 'followers' in parameter:
            data['followers'] = request['followers']
        if 'created_at' in parameter:
            data['created_at'] = request['joined']
        if 'status' in parameter:
            data['status'] = request['status']
        if 'streamer' in parameter:
            data['streamer'] = request['is_streamer']
        return data

    @staticmethod
    def get_player_stats(username, *args):#chess_rapid__last__rating=False, chess_rapid__last__date=False,
    #                      chess_rapid__best__rating=False, chess_rapid__best__date=False, chess_rapid__r__win=False,
    #                      chess_rapid__r__loss=False, chess_rapid__r__draw=False, chess_bullet__last__rating=False,
    #                      chess_bullet__last__date=False, chess_bullet__best__rating=False,
    #                      chess_bullet__best__date=False, chess_bullet__r__win=False, chess_bullet__r__loss=False,
    #                      chess_bullet__r__draw=False, chess_blitz__last__rating=False, chess_blitz__last__date=False,
    #                      chess_blitz__best__rating=False, chess_blitz__best__date=False, chess_blitz__r__win=False,
    #                      chess_blitz__r__loss=False, chess_blitz__r__draw=False, tactics__highest__rating=False,
    #                      tactics__highest__date=False, tactics__lowest__rating=False, tactics__lowest__date=False,
    #                      puzzle_rush__best__total_attempts=False, puzzle_rush__best__score=False):
    #     frame = inspect.currentframe()
    #     parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
    #                  and i != 'username']
    #     if len(args) > 1:
    #         parameter = [i for i in args[0]]
    #     else:
        request = requests.get(f'https://api.chess.com/pub/player/{username}/stats').json()
        data = {}
        pars = [j if j != 'r' else 'record' for j in args[0].split('__')]
        try:
            data[args[0]] = request[pars[0]][pars[1]][pars[2]]
        except:
            print(f'error: {i}')
        return data

    @staticmethod
    def get_player_clubs(username, club_name=None, club_url=None, *args): #clubs=False, in_club=False, ):
        data = {}
        request = requests.get(f'https://api.chess.com/pub/player/{username}/clubs').json()['clubs']
        if 'clubs' == args[0]:
            data['clubs'] = len(request)
        if 'in_club' == args[0] and (club_name or club_url):
            if club_name:
                parameter = club_name.lower()
                data['in_club'] = [i for i in request if i['name'].lower() == parameter]
            elif club_url:
                parameter = club_url
                data['in_club'] = [i for i in request if i['@id'] == parameter]
        return data

    @staticmethod
    def get_player_tournaments(username, *args):#tournaments=False, tournament_wins=False, highest_placement=False,
    #                            lowest_placement=False, max_wins_in_tournament=False, max_losses_in_tournament=False,
    #                            max_draws_in_tournament=False):

        data = {}
        # parameter = [i for i in args[0]]
        request = requests.get(f'https://api.chess.com/pub/player/{username}/tournaments').json()['finished']
        # frame = inspect.currentframe()
        # max_parameter = [i for i in args[0] if 'max' in i]#inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is
        #                  True and 'max' in i]
        # if max_parameter:
        #     for i in max_parameter:
        #         try:
        #             data[i] = [j[i.split('_')[1]] for j in request]
        #         except:
        #             print(f'error: {i}')
        if 'highest_placement' == args[0]:
            data['highest_placement'] = min([j['placement'] for j in request])
        elif 'lowest_placement' == args[0]:
            data['lowest_placement'] = max([j['placement'] for j in request])
        elif 'tournaments' == args[0]:
            data['tournaments'] = len(request)
        elif 'tournament_wins' == args[0]:
            data['tournament_wins'] = len([i for i in request if i['status'] == 'winner'])
        else:
            try:
                data[args[0]] = max([j[args[0].split('_')[1]] for j in request])
            except:
                print(f'error: {args[0]}')
        return data

    @staticmethod
    def get_titled_players(username, title=None, *args):#, is_titled=False):

        data = {}
        if 'is_titled' == args[0] and title:
            data['is_titled'] = False
            request = requests.get(f'https://api.chess.com/pub/titled/{title}').json()['players']
            if username in request:
                data['is_titled'] = True
        return data

    @staticmethod
    def get_leaderboards(username, *args):#in_daily_leaderboard=False, in_live_rapid_leaderboard=False):
        request = requests.get(f'https://api.chess.com/pub/leaderboards').json()
        data = {}
        if 'in_daily_leaderboard' == args[0]:
            data['in_daily_leaderboard'] = [True if i['username'].lower() == username.lower() else False for i in
                                            request['daily']]
        if 'in_live_rapid_leaderboard' == args[0]:
            data['in_live_rapid_leaderboard'] = [True if i['username'].lower() == username.lower() else False for i in
                                                 request['live_rapid']]
        return data


# print(Chesscom.get_player_stats('crazyniga1917', chess_rapid__last__rating=True, chess_rapid__last__date=True,
#                          chess_rapid__best__rating=True, chess_rapid__best__date=True, chess_rapid__r__win=True,
#                          chess_rapid__r__loss=True, chess_rapid__r__draw=True, chess_bullet__last__rating=True,
#                          chess_bullet__last__date=True, chess_bullet__best__rating=True,
#                          chess_bullet__best__date=True, chess_bullet__r__win=True, chess_bullet__r__loss=True,
#                          chess_bullet__r__draw=True, chess_blitz__last__rating=True, chess_blitz__last__date=True,
#                          chess_blitz__best__rating=True, chess_blitz__best__date=True, chess_blitz__r__win=True,
#                          chess_blitz__r__loss=True, chess_blitz__r__draw=True,  tactics__highest__rating=True,
#                          tactics__highest__date=True, tactics__lowest__rating=True, tactics__lowest__date=True,
#                          puzzle_rush__best__total_attempts=True, puzzle_rush__best__score=True))
# d = Chesscom.get_player_stats('crazyniga1917') #player_id, followers, joined, status, is_streamer
# # a=[]
# print('get_player_stats')
# for k,v in d.items():
#     print(k,v)

# print(Chesscom.get_leaderboards())
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
