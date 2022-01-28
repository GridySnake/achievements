from youtube_api import YouTubeDataAPI
from config.common import BaseConfig
import inspect

yt = YouTubeDataAPI(BaseConfig.google_api_key)


class Youtube:
    @staticmethod
    def get_channel_id(channel_name):
        return yt.search(q=channel_name, max_results=1, order_by='relevance')[0]['channel_id']

    @staticmethod
    def get_channel_statistics(channel_id, channel_views=False, channel_videos=False, channel_subscriptions=False,
                               channel_country=False):
        frame = inspect.currentframe()
        parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
                     and i != 'country']
        data = {}
        channel = yt.get_channel_metadata(channel_id)
        if parameter:
            for i in parameter:
                data[i] = channel[i.split('_')[-1][:-1]+'_count']
        if channel_country:
            data['channel_country'] = channel['country']
        return data

    @staticmethod
    def get_count_videos_playlists_of_channel(channel_id, max_playlists_videos=False, min_playlists_videos=False):
        data = {}
        current_playlists = [i['playlist_n_videos'] for i in yt.get_playlists(channel_id)]
        if max_playlists_videos:
            data['max_playlists_videos'] = max(current_playlists)
        if min_playlists_videos:
            data['min_playlists_videos'] = min(current_playlists)
        return data

    @staticmethod
    def get_playlists_of_channel(channel_id):
        playlists_id = [i['playlist_id'] for i in yt.get_playlists(channel_id)]
        return playlists_id

    @staticmethod
    def get_videos_of_playlist(playlist_id):
        videos = {'playlist_id': [], 'video_id': []}
        if type(playlist_id) == str:
            current_videos = yt.get_videos_from_playlist_id(playlist_id)
            videos['playlist_id'] += [playlist_id]
            videos['video_id'] += [i['video_id'] for i in current_videos]
        else:
            for j in playlist_id:
                current_videos = yt.get_videos_from_playlist_id(j)
                videos['playlist_id'] += [j]
                videos['video_id'] += [i['video_id'] for i in current_videos]
        return videos

    @staticmethod
    def get_videos_of_channel(playlist_id):
        if type(playlist_id) == str:
            current_videos = yt.get_videos_from_playlist_id(playlist_id)
            videos = [i['video_id'] for i in current_videos]
        else:
            videos = []
            for j in playlist_id:
                current_videos = yt.get_videos_from_playlist_id(j)
                videos += [i['video_id'] for i in current_videos]
        return videos

    @staticmethod
    def get_video_data(channel_id, max_video_created_at=False, max_video_likes=False, max_video_comments=False,
                       max_video_views=False, min_video_created_at=False, min_video_likes=False,
                       min_video_comments=False, min_video_views=False, account_likes=False, account_comments=False):
        frame = inspect.currentframe()
        account_parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
                             and 'account' in i and 'created_at' not in i]
        max_parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
                         and 'max' in i and 'created_at' not in i]
        min_parameter = [i for i in inspect.getargvalues(frame)[3].keys() if inspect.getargvalues(frame)[3][i] is True
                         and 'min' in i and 'created_at' not in i]
        video_data = [i for i in Youtube.get_videos_of_channel(Youtube.get_playlists_of_channel(channel_id))]
        data = {}
        if account_parameter:
            for i in account_parameter:
                data[i] = sum([j[i.replace('account', 'video')[:-1]+'_count'] for j in video_data])
        if max_parameter:
            for i in max_parameter:
                data[i] = max([j[i.replace('max_', '')[:-1]+'_count'] for j in video_data])
        if min_parameter:
            for i in max_parameter:
                data[i] = min([j[i.replace('min_', '')[:-1]+'_count'] for j in video_data])
        if max_video_created_at:
            data['max_video_created_at'] = max([j['collection_date'] for j in video_data])
        if min_video_created_at:
            data['max_video_created_at'] = min([j['collection_date'] for j in video_data])
        return data
    # @staticmethod
    # def get_comments_of_video(video_id):
    #     comments = {'video_id': [], 'comment_id': [], 'comment_parent_id': [], 'commenter_channel_url': [],
    #                 'commenter_channel_id': [], 'commenter_channel_display_name': [],
    #                 'comment_like_count': [], 'text': [], 'reply_count': []}
    #     if type(video_id) == str:
    #         video = yt.get_video_comments('bvOrQmHnzBE')
    #         comments['video_id'] += [i['video_id'] for i in video]
    #         comments['comment_id'] += [i['comment_id'] for i in video]
    #         comments['comment_parent_id'] += [i['comment_parent_id'] for i in video]
    #         comments['commenter_channel_url'] += [i['commenter_channel_url'] for i in video]
    #         comments['commenter_channel_id'] += [i['commenter_channel_id'] for i in video]
    #         comments['commenter_channel_display_name'] += [i['commenter_channel_display_name'] for i in video]
    #         comments['comment_like_count'] += [i['comment_like_count'] for i in video]
    #         comments['text'] += [i['text'] for i in video]
    #         comments['reply_count'] += [i['reply_count'] for i in video]
    #     else:
    #         for i in video_id:
    #             video = yt.get_video_comments(i)
    #             comments['video_id'] += [i['video_id'] for i in video]
    #             comments['comment_id'] += [i['comment_id'] for i in video]
    #             comments['comment_parent_id'] += [i['comment_parent_id'] for i in video]
    #             comments['commenter_channel_url'] += [i['commenter_channel_url'] for i in video]
    #             comments['commenter_channel_id'] += [i['commenter_channel_id'] for i in video]
    #             comments['commenter_channel_display_name'] += [i['commenter_channel_display_name'] for i in video]
    #             comments['comment_like_count'] += [i['comment_like_count'] for i in video]
    #             comments['text'] += [i['text'] for i in video]
    #             comments['reply_count'] += [i['reply_count'] for i in video]
    #     return comments


#print(Youtube.get_channel_statistics(Youtube.get_channel_id('Davidich D3'))) #view_count, video_count, subscription_count
# print(Youtube.get_playlists_of_channel(Youtube.get_channel_id('Davidich D3'))) #playlist_name, playlist_id, count_videos
# print(Youtube.get_videos_of_playlist(Youtube.get_playlists_of_channel(Youtube.get_channel_id('Davidich D3')))) #playlist_id, video_id
# print(Youtube.get_video_data(video_id='wIzU5RrwfUI'))
# print(Youtube.get_comments_of_video(Youtube.get_videos_of_playlist(Youtube.get_playlists_of_channel(Youtube.get_channel_id('Davidich D3'))['playlist_id'])['video_id'][0])) #comments_info
