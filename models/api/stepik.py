import requests
from config.common import BaseConfig


class Stepik:
    @staticmethod
    def get_user_info(user_id):
        response = requests.get(f'https://stepik.org:443/api/users/{user_id}').json()
        user = {'user_id': response['users'][0]['profile'], 'is_organization': response['users'][0]['is_organization'],
                'full_name': response['users'][0]['full_name'], 'city': response['users'][0]['city'],
                'knowledge': response['users'][0]['knowledge'], 'knowledge_rank': response['users'][0]['knowledge_rank'],
                'reputation': response['users'][0]['reputation'], 'reputation_rank': response['users'][0]['reputation_rank'],
                'solved_steps_count': response['users'][0]['solved_steps_count'],
                'created_courses_count': response['users'][0]['created_courses_count'],
                'created_lessons_count': response['users'][0]['created_lessons_count'],
                'issued_certificates_count': response['users'][0]['issued_certificates_count'],
                'followers_count': response['users'][0]['followers_count']}
        return user