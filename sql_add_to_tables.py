from sqlalchemy import create_engine
import datetime
from config.common import BaseConfig
import pandas as pd

engine = create_engine(BaseConfig.database_url)

# engine.execute("""insert INTO achi_conditions (condition_id, parameter, value, achi_condition_group_id) values(
#                           0, 'name', 'Aleksandr', 0)
#                          """)
# engine.execute("""insert INTO achi_condition_groups (achi_condition_group_id, achi_condition_group_name, achi_condition_group_description) values(
#                           0, 'user info', 'Any public information about user')
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
