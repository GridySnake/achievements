from youtube_api import YouTubeDataAPI
from config.common import BaseConfig

yt = YouTubeDataAPI(BaseConfig.google_api_key)


class Youtube:
    @staticmethod
    def get_channel_id(channel_name):
        return yt.search(q=channel_name, max_results=1, order_by='relevance')[0]['channel_id']

    @staticmethod
    def get_channel_statistics(channel_id):
        channel = {}
        current_channel = yt.get_channel_metadata(channel_id)
        for i in ['title', 'view_count', 'video_count', 'subscription_count', 'country']:
            channel[i] = current_channel[i]
        return channel

    @staticmethod
    def get_playlists_of_channel(channel_id):
        playlists = {'playlist_name': [], 'playlist_id': [], 'playlist_n_videos': []}
        current_playlists = yt.get_playlists(channel_id)
        for i in range(len(current_playlists)):
            playlists['playlist_name'] += [current_playlists[i]['playlist_name']]
            playlists['playlist_id'] += [current_playlists[i]['playlist_id']]
            playlists['playlist_n_videos'] += [current_playlists[i]['playlist_n_videos']]
        return playlists

    @staticmethod
    def get_videos_of_playlist(playlist_id):
        videos = {'playlist_id': [], 'video_id': []}
        if type(playlist_id) == str:
            current_videos = yt.get_videos_from_playlist_id(playlist_id)
            videos['video_id'] += [i for i in range(len(current_videos))]
            videos['video_id'] += [i['video_id'] for i in current_videos]
        else:
            for j in playlist_id:
                current_videos = yt.get_videos_from_playlist_id(j)
                videos['playlist_id'] += [j]
                videos['video_id'] += [i['video_id'] for i in current_videos]
        return videos

    @staticmethod
    def get_comments_of_video(video_id):
        comments = {'video_id': [], 'comment_id': [], 'comment_parent_id': [], 'commenter_channel_url': [],
                    'commenter_channel_id': [], 'commenter_channel_display_name': [],
                    'comment_like_count': [], 'text': [], 'reply_count': []}
        if type(video_id) == str:
            video = yt.get_video_comments('bvOrQmHnzBE')
            comments['video_id'] += [i['video_id'] for i in video]
            comments['comment_id'] += [i['comment_id'] for i in video]
            comments['comment_parent_id'] += [i['comment_parent_id'] for i in video]
            comments['commenter_channel_url'] += [i['commenter_channel_url'] for i in video]
            comments['commenter_channel_id'] += [i['commenter_channel_id'] for i in video]
            comments['commenter_channel_display_name'] += [i['commenter_channel_display_name'] for i in video]
            comments['comment_like_count'] += [i['comment_like_count'] for i in video]
            comments['text'] += [i['text'] for i in video]
            comments['reply_count'] += [i['reply_count'] for i in video]
        else:
            for i in video_id:
                video = yt.get_video_comments(i)
                comments['video_id'] += [i['video_id'] for i in video]
                comments['comment_id'] += [i['comment_id'] for i in video]
                comments['comment_parent_id'] += [i['comment_parent_id'] for i in video]
                comments['commenter_channel_url'] += [i['commenter_channel_url'] for i in video]
                comments['commenter_channel_id'] += [i['commenter_channel_id'] for i in video]
                comments['commenter_channel_display_name'] += [i['commenter_channel_display_name'] for i in video]
                comments['comment_like_count'] += [i['comment_like_count'] for i in video]
                comments['text'] += [i['text'] for i in video]
                comments['reply_count'] += [i['reply_count'] for i in video]
        return comments


# print(Youtube.get_channel_statistics(Youtube.get_channel_id('Davidich D3')))
# print(Youtube.get_playlists_of_channel(Youtube.get_channel_id('Davidich D3')))
# print(Youtube.get_videos_of_playlist(Youtube.get_playlists_of_channel(Youtube.get_channel_id('Davidich D3'))['playlist_id']))
# print(Youtube.get_comments_of_video(Youtube.get_videos_of_playlist(Youtube.get_playlists_of_channel(Youtube.get_channel_id('Davidich D3'))['playlist_id'])['video_id'][0]))
