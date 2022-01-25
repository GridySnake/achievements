from sqlalchemy import create_engine
import datetime
from config.common import BaseConfig
import pandas as pd

engine = create_engine(BaseConfig.database_url)

# engine.execute("""insert INTO achi_conditions (condition_id, parameter, value, achi_condition_group_id) values(
#                           0, 'name', 'Aleksandr', 0)
#                          """)
# engine.execute("""insert INTO achi_condition_groups (achi_condition_group_id, achi_condition_group_name, achi_condition_group_description) values(
#                           2, 'Geolocation', 'To verify need to be in this location and use geolocation')
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
df = pd.read_csv('C:/Users/mamed/PycharmProjects/achievements/static/All_Occupations.csv', sep=',')
print(df.columns)
df.drop(['Code'], axis=1, inplace=True)
n = 24
k = 0
print(len(df['Occupation'].unique()))
print(len(df['Job Family'].unique()))
# df['subsphere_id'] = range(23)
# sphere_name
# subsphere_name
df_sphere = pd.DataFrame()
df_sphere['sphere_id'] = list(range(0, len(df['Job Family'].unique()), 1))
df_sphere['Job Family'] = df['Job Family'].unique()
# print(df_sphere)
# df['subsphere_id'] = ''
# df['sphere_id'] = ''
# for i in range(len(df['Occupation'])):
# print(df)
df['subsphere_id'] = list(range(23, len(df['Occupation'])+23, 1))
df_1 = df.merge(df_sphere, how='inner', on='Job Family')
# pd.set_option('display.max_columns', None)
# print(df_1)
d_finish = {'subsphere_id': [], 'subsphere_name': [], 'sphere_id': [], 'sphere_name': []}
d_finish['subsphere_id'] = df_1['subsphere_id']
d_finish['subsphere_name'] = df_1['Occupation']
d_finish['sphere_id'] = df_1['sphere_id']
d_finish['sphere_name'] = df_1['Job Family'].copy()
df_finish = pd.DataFrame(d_finish)
# pd.set_option('display.max_columns', None)
# print(df_finish)
df_finish.to_sql('spheres',
                    create_engine('postgresql://gachi_achi:achi_for_gachi@204.2.63.15:10485/achievements'),
                    if_exists='append', method='multi', index=False)


