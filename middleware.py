from aiohttp.web import json_response, middleware


@middleware
async def auth_middleware(request, handler):
    print(handler.__name__)
    print(request.cookies)
    if handler.__name__ in ['login_kek', '_preflight_handler', 'signup']:
        return await handler(request)

    auth_cookie = request.cookies.get('user')
    if auth_cookie is not None:
        return await handler(request)
    else:
        return json_response({'error': 'You are not authorized'}, status=401)