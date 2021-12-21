import base64
import logging
import aiohttp_jinja2
import jinja2
from aiohttp import web
import asyncpgsa
# from swagger_ui import aiohttp_api_doc
from aiohttp_swagger import *
# from aiohttp_swaggerify import swaggerify
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from routes.base import setup_routes, setup_static_routes
from config.common import BaseConfig
from models.user import UserGetInfo


async def current_user_ctx_processor(request):
    session = await get_session(request)
    user = None
    is_anonymous = True
    user_id = None
    if 'user' in session:
        user_id = session['user']['id']
        user = await UserGetInfo.get_user_by_id(user_id=user_id)
        if user:
            is_anonymous = not bool(user)
    return dict(current_user=user, is_anonymous=is_anonymous, user_id=user_id)


@web.middleware
async def user_session_middleware(request, handler):
    request.session = await get_session(request)
    response = await handler(request)
    return response


def setup_middlewares(app):
    app.middlewares.append(user_session_middleware)


def main():
    app = web.Application(debug=True)

    secret_key = base64.urlsafe_b64decode(BaseConfig.secret_key)
    setup(app, EncryptedCookieStorage(secret_key))

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(package_name='main', package_path='templates'),
        context_processors=[current_user_ctx_processor])

    setup_routes(app)
    setup_static_routes(app)

    # async def ping(request):
    #     """
    #     ---
    #     description: This end-point allow to test that service is up.
    #     tags:
    #     - Health check
    #     produces:
    #     - text/plain
    #     responses:
    #         "200":
    #             description: successful operation. Return "pong" text
    #         "405":
    #             description: invalid HTTP Method
    #     """
    #     return web.Response(text="pong")
    #
    # app.router.add_route('GET', "/ping", ping)

    # setup_swagger(app, swagger_url="/api/v1/doc", ui_version=2)
    # setup_swagger(app)
    setup_middlewares(app)
    # aiohttp_api_doc(app, config_path='./conf/test.yaml', url_prefix='/api/doc', title='API doc')
    app['config'] = BaseConfig
    app['db'] = asyncpgsa.create_pool(
        host=BaseConfig.host,
        port=BaseConfig.port,
        database=BaseConfig.database_name,
        user=BaseConfig.user,
        password=BaseConfig.password
    )

    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, host="127.0.0.1")


if __name__ == '__main__':
    main()
