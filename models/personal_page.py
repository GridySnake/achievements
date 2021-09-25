# import hashlib
# import asyncpgsa
# from config.common import BaseConfig
# import asyncpg
# from asyncpgsa import pg
# database = asyncpgsa.create_pool(
#         host=BaseConfig.host,
#         port=BaseConfig.port,
#         database=BaseConfig.database_name,
#         user=BaseConfig.user,
#         password=BaseConfig.password
#     )
#
#
# class Persona:
#     @staticmethod
#     async def get_user_by_id(user_id: str):
#         conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
#         user = await conn.fetchrow(f"""
#                 SELECT users.*, avatars.url
#                 FROM users
#                 LEFT JOIN avatars ON avatars.user_id = users.id
#                 WHERE id = '{user_id}'
#                 """)
#         user = dict(user)
#         if user:
#             user['id'] = int(user['id'])
#             return user
#         else:
#             return None
#
#     @staticmethod
#     async def create_new_user(data):
#         email = data['email']
#         conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
#         user = await conn.fetchrow(f"""
#                 SELECT *
#                 FROM users
#                 WHERE email = '{email}'
#                 """)
#         if user is not None:
#             return dict(error='user with email {} exist'.format(email))
#
#         if data['first_name'] and data['last_name'] and data['password']:
#             data = dict(data)
#             #data['password'] = hashlib.sha256(data['password'].encode('utf8')).hexdigest()
#             id = await conn.fetchrow(f"""SELECT MAX(id) FROM users""")
#             id = int(dict(id)['max']) + 1
#             result = await conn.execute(f"""
#                 insert INTO users (id, first_name, last_name, email, password) values(
#                 {id}, '{data['first_name']}', '{data['last_name']}', '{data['email']}', '{data['password']}')
#                 """)
#             return result
#         else:
#             return dict(error='Missing user data parameters')
#
#     @staticmethod
#     async def save_avatar_url(user_id: str, url: str):
#         conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
#         if url is not None and user_id is not None:
#             us_id = await conn.fetchrow(f"""SELECT user_id FROM avatars WHERE user_id = {user_id}""")
#             #url = 'C:/Users/kunil/PycharmProjects/social-network/static/avatars/' + url
#             if us_id is None:
#                 avatar_id = await conn.fetchrow(f"""SELECT MAX(avatar_id) FROM avatars""")
#                 avatar_id = int(dict(avatar_id)['max']) + 1
#                 await conn.execute(f"""
#                                 insert INTO avatars (avatar_id, user_id, url) values(
#                                 {avatar_id}, {user_id}, '{url}')
#                                 """)
#             else:
#                 await conn.execute(f"""
#                                                 UPDATE avatars
#                                                 SET url = '{url}'
#                                                 WHERE user_id = {user_id}
#                                                 """)
#             return url
#
#     @staticmethod
#     async def get_user_friends_suggestions(user_id: str, limit=20):
#         conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
#         users = await conn.fetch(f"""SELECT u.*
#                                      FROM users as u
#                                      WHERE u.id not in (SELECT unnest(friend)
#                                                        FROM friends
#                                                        WHERE user_id = {user_id})
#                                      AND u.id <> {user_id}
#                                      LIMIT {limit}
#         """)
#         return users
#
#     @staticmethod
#     async def get_user_friends_names(user_id: str, limit=20):
#         conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
#         users = await conn.fetch(f"""SELECT u.*
#                                      FROM users as u
#                                      WHERE u.id in (SELECT unnest(f.friend)
#                                                        FROM friends as f
#                                                        WHERE f.user_id = {user_id})
#                                      LIMIT {limit}
#         """)
#         return users
#
#     @staticmethod
#     async def get_user_friends(user_id: str, limit=20):
#         conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
#         user_friends = await conn.fetchrow(f"""SELECT friend FROM friends WHERE user_id = {user_id} LIMIT {limit}""")
#         return user_friends
#
#     @staticmethod
#     async def add_friend(user_id: str, friend_id: str):
#         conn = await asyncpg.connect('postgresql://postgres:12041999alex@localhost:5433/demo')
#         friends = User.get_user_friends(user_id)
#         if friends is not None:
#             friends = await conn.fetchrow(f"""SELECT friend FROM friends WHERE user_id = {user_id} AND {friend_id} = ANY(friend)""")
#             if friends is not None:
#                 pass
#             else:
#                 await conn.execute(
#                 f"""UPDATE friends
#                     SET friend = array_append(friend, {friend_id})
#                     WHERE user_id = {user_id}
#                    """)
#         else:
#             await conn.execute(
#                 f"""insert INTO friends (user_id, friend) values(
#            {user_id}, ARRAY[{friend_id}])
# """)
