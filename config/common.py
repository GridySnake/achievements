import pathlib


class BaseConfig:

    debug = True
    app_name = 'Social Network'
    secret_key = b'TyzLMReLCWUiPsTFMActw_0dtEU7kAcFXHNYYm64DNI='

    PROJECT_ROOT = pathlib.Path(__file__).parent.parent
    STATIC_DIR = str(PROJECT_ROOT / 'static')
    database_url = 'postgres:12041999alex@localhost:5433/demo'
    host = 'localhost'
    port = 5433
    database_name = 'demo'
    user = 'postgres'
    password = '12041999alex'

