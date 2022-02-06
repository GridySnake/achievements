import datetime
import myfitnesspal
import math
import inspect

login = 'crazynigga1917'
password = '12041999alex'


class Fitnesspal:
    @staticmethod
    def login(user_name, password):
        client = myfitnesspal.Client(user_name, password)
        return client

    @staticmethod
    def day_metrics(client, date=datetime.date.today(), calories=False, carbohydrates=False, fat=False, protein=False,
                    sodium=False, sugar=False, meals_name=False, water=False, complete_goal=False):
        frame = inspect.currentframe()
        parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
                     and i in ['calories', 'carbohydrates', 'fat', 'protein', 'sodium', 'sugar']]
        data = {}
        day = client.get_date(date)
        if parameter:
            for j in parameter:
                try:
                    data[j] = sum([i[0][j] for i in day.meals])
                except:
                    print(f'error: {i}')
        if water:
            data['water'] = int(day.water)
        if complete_goal:
            data['complete_goal'] = day.complete_goal
        if meals_name:
            data['meals_name'] = [i[0].name for i in day.meals]
        return data

    @staticmethod
    def user_info(client, date=datetime.date.today(), created_at=False, exercise_minutes=False, exercise_burned=False,
                  start_weight=False, current_weight=False, height=False, activity_type=False):
        metadata = client.user_metadata
        user_data = metadata['profiles'][0]
        data = {}
        if created_at:
            data['created_at'] = metadata['account']['created_at'].split('T')[0]
        elif exercise_minutes:
            data['exercise_minutes'] = sum(
                [i['nutrition_information']['minutes'] for i in client.get_date(date).exercises[0].get_as_list() if
                 i['nutrition_information']['minutes'] is not None])
        elif exercise_burned:
            data['exercise_burned'] = sum(
                [i['nutrition_information']['calories burned'] for i in client.get_date(date).exercises[0].get_as_list()
                 if i['nutrition_information']['calories burned'] is not None])
        elif start_weight:
            data['start_weight']: int(user_data['starting_weight']['value'])
            data['unit'] = metadata['unit_preferences']['weight']
        elif current_weight:
            data['current_weight'] = client.get_measurements('Weight', date)
            data['unit'] = metadata['unit_preferences']['weight']
        elif height:
            if metadata['unit_preferences']['height'] == 'centimeters':
                data['height'] = math.ceil(user_data['height']['value'] / 0.39368021)
            else:
                data['height'] = math.ceil(user_data['height']['value'])
            data['unit'] = metadata['unit_preferences']['height']
        elif activity_type:
            data['activity_type'] = user_data['activity_factor']
        return data


# print(Fitnesspal.day_metrics(Fitnesspal.login(login, password), calories=True))
