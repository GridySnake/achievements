import requests
# from config.common import BaseConfig
import inspect


class Stepik:
    @staticmethod
    def get_user_info(user_id, *args):#organization=False, knowledge_rank=False, reputation_rank=False, knowledge=False,
    #                   reputation=False, solved_steps=False, created_courses=False, created_lessons=False,
    #                   issued_certificates=False, followers=False, created_at=False):
    #     frame = inspect.currentframe()
        parameter = [i for i in args
                     if i not in ['user_id', 'created_at', 'solved_steps', 'created_courses', 'created_lessons',
                                   'issued_certificates', 'followers']]

        parameter_count = [i for i in args if i not in ['user_id', 'created_at', 'organization', 'knowledge_rank', 'reputation_rank',
                                   'knowledge', 'reputation', 'is_organization']]
    #     parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
    #                  and i not in ['user_id', 'created_at', 'solved_steps', 'created_courses', 'created_lessons',
    #                                'issued_certificates', 'followers']]
    #     parameter_count = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
    #                  and i not in ['user_id', 'created_at', 'organization', 'knowledge_rank', 'reputation_rank',
    #                                'knowledge', 'reputation']]
        data = {}
        response = requests.get(f'https://stepik.org:443/api/users/{user_id}').json()
        response = response['users'][0]
        if parameter:
            for i in parameter:
                try:
                    data[i] = response[i]
                except:
                    print(f'error: {i}')
        if parameter_count:
            for i in parameter_count:
                data[i] = response[str(i+'_count')]
        if 'created_at' in args[0]:
            data['created_at'] = response['join_date'].split('T')[0]
        return data


# print(Stepik.get_user_info(43723297, ('solved_steps')))