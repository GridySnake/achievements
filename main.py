import base64
import logging
import asyncpg
import asyncio
from aiohttp import web
import asyncpgsa
import aiohttp_cors
# from swagger_ui import aiohttp_api_doc
from aiohttp_swagger import *
# from aiohttp_swaggerify import swaggerify
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from middleware import auth_middleware
from routes.base import setup_routes, setup_static_routes
from config.common import BaseConfig


async def setup_middlewares(app):
    app.middlewares.append(auth_middleware)


async def create_app():
    app = web.Application(client_max_size=1000000000000000000, debug=True)

    secret_key = base64.urlsafe_b64decode(BaseConfig.secret_key)
    setup(app, EncryptedCookieStorage(secret_key))
    cors_accept = aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_methods="*",
        allow_headers="*",
    )
    cors = aiohttp_cors.setup(app, defaults={'http://localhost:3000': cors_accept})
    setup_routes(app)
    for route in list(app.router.routes()):
        cors.add(route)
    setup_static_routes(app)
    await setup_middlewares(app)
    app['config'] = BaseConfig
    # app['db'] = asyncpgsa.create_pool(
    #     host=BaseConfig.host,
    #     port=BaseConfig.port,
    #     database=BaseConfig.database_name,
    #     user=BaseConfig.user,
    #     password=BaseConfig.password
    # )
    app['pool'] = await asyncpg.create_pool(dsn=BaseConfig.database_url, max_size=30)
    logging.basicConfig(level=logging.DEBUG)
    return app



# if __name__ == '__main__':
#
# loop = asyncio.get_event_loop()
# app = loop.run_until_complete()
web.run_app(app=create_app(), host="localhost", port=8082)
