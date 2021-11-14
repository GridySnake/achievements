import base64
import logging
import aiohttp_jinja2
import jinja2
from aiohttp import web
import asyncpgsa
from aiohttp_swaggerify import swaggerify
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from routes.base import setup_routes, setup_static_routes
from config.common import BaseConfig
from models.user import User


async def current_user_ctx_processor(request):
    session = await get_session(request)
    user = None
    is_anonymous = True
    user_id = None
    if 'user' in session:
        user_id = session['user']['id']
        user = await User.get_user_by_id(user_id=user_id)
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
    setup_middlewares(app)

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
