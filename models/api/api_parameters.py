class ChesscomParameter:
    @staticmethod
    def get_player_profile(username, followers, created_at, status, streamer):
        return None

    @staticmethod
    def get_player_stats(username, chess_rapid__last__rating, chess_rapid__last__date,
                         chess_rapid__best__rating, chess_rapid__best__date, chess_rapid__r__win,
                         chess_rapid__r__loss, chess_rapid__r__draw, chess_bullet__last__rating,
                         chess_bullet__last__date, chess_bullet__best__rating,
                         chess_bullet__best__date, chess_bullet__r__win, chess_bullet__r__loss,
                         chess_bullet__r__draw, chess_blitz__last__rating, chess_blitz__last__date,
                         chess_blitz__best__rating, chess_blitz__best__date, chess_blitz__r__win,
                         chess_blitz__r__loss, chess_blitz__r__draw, tactics__highest__rating,
                         tactics__highest__date, tactics__lowest__rating, tactics__lowest__date,
                         puzzle_rush__best__total_attempts, puzzle_rush__best__score):
        return None

    @staticmethod
    def get_player_clubs(username, clubs, in_club, club_name, club_url):
        return None

    @staticmethod
    def get_player_tournaments(username, tournaments, tournament_wins, highest_placement,
                               lowest_placement, max_wins_in_tournament, max_losses_in_tournament,
                               max_draws_in_tournament):
        return None

    @staticmethod
    def get_titled_players(username, title, is_titled):
        return None

    @staticmethod
    def get_leaderboards(username, in_daily_leaderboard, in_live_rapid_leaderboard):
        return None


class FitnesspalParameter:
    @staticmethod
    def login(user_name, password):
        return None

    @staticmethod
    def day_metrics(client, date, calories, carbohydrates, fat, protein,
                    sodium, sugar, meals_name, water, complete_goal):
        return None

    @staticmethod
    def user_info(client, date, created_at, exercise_minutes, exercise_burned,
                  start_weight, current_weight, height, activity_type):
        return None


class SteamParameter:
    @staticmethod
    def login(username, password):
        return None

    @staticmethod
    def get_user_info(steam_id, created_at, communities):
        return None

    @staticmethod
    def get_friends(steam_id, friends):
        return None

    @staticmethod
    def get_app_id_via_app_name(app_name):
        return None

    @staticmethod
    def get_app_name_via_app_id(app_id):
        return None

    @staticmethod
    # todo: сделать для разных игр разные параметры
    def get_game_stats(steam_id, app_id):
        return None

    @staticmethod
    def get_games(steam_id, games, total_play_time, game_id, game_play_time):
        return None


class StepikParameter:
    @staticmethod
    def get_user_info(user_id, organization, knowledge_rank, reputation_rank, knowledge,
                      reputation, solved_steps, created_courses, created_lessons,
                      issued_certificates, followers, created_at):
        return None


class TwitchParameter:
    @staticmethod
    def get_user_info(username, account_views, account_created_at, account_broadcaster_type):
        return None

    @staticmethod
    def get_user_videos_info(username, video_views, video_type, video_duration, video_created_at):
        return None

    @staticmethod
    def get_user_following_info(username, followings, follow_user, followed_at):
        return None


class YoutubeParameter:
    @staticmethod
    def get_channel_id(channel_name):
        return None

    @staticmethod
    def get_channel_statistics(channel_id, channel_views, channel_videos, channel_subscriptions,
                               channel_country):
        return None

    @staticmethod
    def get_count_videos_playlists_of_channel(channel_id, max_playlists_videos, min_playlists_videos):
        return None

    @staticmethod
    def get_playlists_of_channel(channel_id):
        return None

    @staticmethod
    def get_videos_of_playlist(playlist_id):
        return None

    @staticmethod
    def get_videos_of_channel(playlist_id):
        return None

    @staticmethod
    def get_video_data(channel_id, max_video_created_at, max_video_likes, max_video_comments,
                       max_video_views, min_video_created_at, min_video_likes,
                       min_video_comments, min_video_views, account_likes, account_comments):
        return None
