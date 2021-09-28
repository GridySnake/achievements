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
