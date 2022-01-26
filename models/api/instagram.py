from changed_pack.instabot import Bot
from InstagramAPI import InstagramAPI
import time
import traceback
import pandas as pd
import datetime
from config.common import BaseConfig


class MyInstaCrawler(InstagramAPI):
    """
    Want to have a direct control over the instaAPI. When the users are loaded from api, the best way is to store
    them in the queue, where it would have listeners - parsers that would do next job.
    """
    def __init__(self, username, password):
        super().__init__(username, password)

    def getTotalFollowers(self, usernameId):
        import datetime
        next_max_id = ''
        followers = []
        while 1:
            try:
                if self.getUserFollowers(usernameId, next_max_id):
                    temp = self.LastJson
                    for item in temp["users"]:
                        followers.append(item)
                    print('Followers: %s ' % len(followers))
                    temp['collected_date'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    if temp.get("big_list") is None:
                        return followers
                    elif temp['big_list'] is False:
                        return followers
                    next_max_id = temp["next_max_id"]
            except:
                print(traceback.format_exc())
                print("Sleeping 10 secs")
                time.sleep(10)


class Instagram:

    @staticmethod
    def login_instagram(username, password):
        bot = Bot()
        bot.login(username=username, password=password, use_cookie=False)
        return bot

    @staticmethod
    def get_count_of_followers(username, password):
        try:
            bot = Instagram.login_instagram(username, password)
            user_followers = bot.get_user_followers(username)
            count_of_followers = len(user_followers)
            return count_of_followers
        except ConnectionError:
            print('Username or password is incorrect')

    @staticmethod
    def get_most_likes(username_input, password_input,
                       username=BaseConfig.instagram_username, password=BaseConfig.instagram_password):
        try:
            bot = Instagram.login_instagram(username_input, password_input)
            id = bot.get_user_id_from_username(username_input)
            ic = MyInstaCrawler(username, password)
            ic.login()
            arg = id
            total_results = []
            results = ic.getTotalUserFeed(arg)
            if len(results) != 0:
                username = results[0]['user']['username']
                for r in results:
                    try:
                        reduced_r = {}
                        date = datetime.datetime.fromtimestamp(r['taken_at'])
                        date = date.strftime("%Y-%m-%d"'T'"%H:%M:%S"'Z')
                        caption = r['caption']
                        caption_text = ''
                        if caption is not None:
                            caption_text = caption['text']
                        view_count = 0
                        if r['media_type'] == 2:
                            if r.get('view_count'):
                                view_count = int(r['view_count'])
                        reduced_r['created_time'] = date
                        reduced_r['user.username'] = username
                        reduced_r['caption.text'] = caption_text
                        reduced_r['likes.count'] = r['like_count']
                        reduced_r['video_views'] = view_count
                        reduced_r['comments.count'] = r['comment_count']
                        reduced_r['link'] = 'https://instagram.com/p/' + r['code']
                        total_results.append(reduced_r)
                    except Exception as e:
                        print(e)
            df = pd.DataFrame(total_results)
            likes_max_count = df['likes.count'].max()
            video_views_max = df['video_views'].max()
            return likes_max_count, video_views_max
        except ConnectionError:
            print('Username or password is incorrect')

# print(Instagram.get_count_of_followers(username='ivan_qwerty', password='ivanpivan'))