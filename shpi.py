# import pandas as pd
# df = pd.read_csv('https://docs.google.com/spreadsheets/d/1IfGwdFNR59b0lbpRK_2MM8sx3GXdpjhZ8RmdKVVG9Ng/export?format=csv')
# df = df[[i for i in df.columns[1:3]]]
# dict_result = {'email': [], 'result': []}
# dict_result['email'] = [i for i in df[df.columns[0]]]
# dict_result['result'] = [int(i.split(' / ')[0]) for i in df[df.columns[1]]]
# print(dict_result)

# print("""
# date, created_at, exercise_minutes, exercise_burned,
# start_weight, current_weight, height, activity_type
# """.replace('=False', '').replace(',\n', '').replace(', ', ''))


from config.services_our_api import ServicesConfig
ser_id = 0
parameter = 'puzzle_rush__best__total_attempts'
param = 'tactics__highest__date', 'chess_blitz__last__rating'

# func_name = [i for i in ServicesConfig.service_functions.keys() if ServicesConfig.service_classes[ser_id].__name__ in i and parameter in i]
# print(ServicesConfig.service_functions[func_name[0]]('crazyniga1917', param))

# todo: need params not T/F:
#   Chess.com:
#       1. username - all functions
#       2. title
#       3. club_name/club_url
#   MyFitnesspal:
#       1. user_name, password - login
#       2. date - optional = now()
#   Steam:
#       1. username, password - login
#       2. game_id
#   Stepik:
#       1. username
#   Twitch:
#       1. username
#       2. follow_user
#   Youtube:
#       1. channel_id
#