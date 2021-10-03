from sqlalchemy import create_engine
import datetime
from config.common import BaseConfig

engine = create_engine(BaseConfig.database_url)

t = engine.execute(f"""
SELECT verifying_token
FROM authentication
Where verifying_token IS NOT null
""").fetchall()
print(t[0][0])

# engine.execute('''
# insert INTO users_main (user_id, user_name, email, phone) values(1, 'Abba', 'APatt@tatoine.ga', '12345');
# ''')

# engine.execute('''
# insert INTO users (id, first_name, last_name, email, password) values(NEXT(), 'Abba', 'Patt', 'APatt@tatoine.ga', '12345');
# ''')
# engine.execute("""insert INTO friends (user_id, friend) values(
#                           1, ARRAY []::integer[])
#                          """)
# engine.execute("""insert INTO achievements (achievement_id, user_id, name, description) values(
#                            2, ARRAY [0, 2], 'Never sleep', 'Code and do not sleep')
#                          """)

# engine.execute("""insert INTO avatars (avatar_id, user_id, url) values(
#                             0, 0, 'C:/Users/kunil/PycharmProjects/social-network/static/avatars/номер.png')""")

# engine.execute(f"""
#                         insert INTO posts (post_id, user_id, message, date_created) values(
#                         0, 0, 'Hello, world!', '{datetime.datetime.now()}')
#                         """)
# engine.execute(f"""
#                             insert INTO messages (message_id, from_user, to_user, message, date_created) values(
#                             1, 2, 0, 'Hi, Bratinok:)', '{datetime.datetime.now()}')
#                             """)

# post = engine.execute(f"""
#             SELECT MAX(post_id)
#             FROM posts
#             WHERE user_id = '0'
#             LIMIT 20
#             """).fetchall()
# print(post)
# ava = engine.execute(f"""
# Select * from users_main
# """).fetchall()
# print(ava)
