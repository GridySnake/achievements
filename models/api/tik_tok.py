from TikTokApi import TikTokApi


class TikTok:
    @staticmethod
    def change_human_type_to_int(n):
        digit = float("".join(filter(lambda d: str.isdigit(d) or d == '.', n)))
        if ('K' in n):
            p = digit*1000
            return p
        if ('M' in n):
            p = digit * 1000000
            return p
        if ('B' in n):
            p = digit * 1000000000
            return p
        if ('T' in n):
            p = digit * 1000000000000
            return p

    @staticmethod
    def get_likes_and_followers_by_username(username):
        api = TikTokApi.get_instance(custom_verifyFp=None, use_test_endpoints=True,
                                     use_selenium=False)
        data = api.get_user(username=username)
        like_fans = data['seoProps']['metaParams']['description']
        l = like_fans.split(' Likes.')[0].split(' | ')[1]
        f = like_fans.split(' Likes.')[1].split(' Fans.')[0]
        likes = int(TikTok.change_human_type_to_int(l))
        fans = int(TikTok.change_human_type_to_int(f))
        return likes, fans


if __name__ == '__main__':
    print(TikTok.get_likes_and_followers_by_username(username='karna.val'))