import pathlib


class BaseConfig:

    debug = True
    app_name = 'Social Network'
    secret_key = b'TyzLMReLCWUiPsTFMActw_0dtEU7kAcFXHNYYm64DNI='

    PROJECT_ROOT = pathlib.Path(__file__).parent.parent
    STATIC_DIR = str(PROJECT_ROOT / 'static')
    database_url = 'postgresql://gachi_achi:achi_for_gachi@204.2.63.15:10485/achievements'
    host = '204.2.63.15'
    port = 10485
    database_name = 'achievements'
    user = 'gachi_achi'
    password = 'achi_for_gachi'
    email_mail = 'kunilovalex@gmail.com'
    email_user = 'kunilovalex@gmail.com'
    email_password = '12041999alex'
    smtp_server = 'smtp.gmail.com'
    email_port = 465
    twitch_client_id = 'blif82wvvraojfm84xp82fam1ljnii'
    twitch_client_secret = 'abqm6gspq4lhaddede83szum1u0v2b'
    google_api_key = 'AIzaSyAmn8JyIJIkHhqC6IaVLrN-TiTvdHXpwQo'
    google_client_id = '206162279954-q3mm2t5dqmnmdkoiaq28qh0as824f9jr.apps.googleusercontent.com'
    google_client_secret = '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'