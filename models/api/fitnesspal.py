import datetime
import myfitnesspal
import math

login = 'crazynigga1917'
password = '12041999alex'
class Fitnesspal:
    @staticmethod
    def login(user_name, password):
        client = myfitnesspal.Client(user_name, password)
        return client

    @staticmethod
    def day_metrics(client, date=datetime.date.today()):
        date = str(date).split('-')
        day = client.get_date(date[0], date[1], date[2])
        return {'meals': {i.name: i.totals for i in day.meals}, 'water': int(day.water), 'compleate_goal': day.complete,
                'food': {i.name: i.totals for i in day.entries}}

    @staticmethod
    def user_info(client, date=datetime.date.today()):
        user_data = client.user_metadata['profiles'][0]
        print(user_data)
        return {'current_weight': int(client.get_measurements()[date]),
                'weight_start': int(user_data['starting_weight']['value']),
                'height': math.ceil(user_data['height']['value'] / 0.39368021),
                'activity_type': user_data['activity_factor']}


# print(Fitnesspal.user_info(Fitnesspal.login(login, password)))