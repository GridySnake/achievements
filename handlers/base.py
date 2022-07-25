import hashlib
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.user import *
from config.common import BaseConfig
from smtplib import SMTP_SSL
from email.parser import Parser
from email.policy import default
import json
from aiohttp.web import json_response
import os
from models.images import Images


async def auth(request):
    user = request.cookies['user']
    payload = json.loads(user)
    return json_response(payload)


async def login(request):
    data = await request.json()
    if '@' in data['email']:
        type = 'email'
    else:
        type = 'phone'
    pool = request.app['pool']
    async with pool.acquire() as conn:
        user = await UserGetInfo.get_user_by_email_phone(email=data['email'], type=type, conn=conn)
    # if user == 'verify':
    #     return web.HTTPFound(location=self.app.router['verify'].url_for())
    if user and user['password'] == hashlib.sha256(data['password'].encode('utf8')).hexdigest():
        del user['password']
        payload = json.dumps(user)
        resp = json_response(user)
        resp.set_cookie(
            name="user",
            value=payload,
            httponly=True,
            domain='localhost',
            max_age=36000000
        )
        return resp
    else:
        return json_response({"error": "User is not found"})


async def upload_group_avatar(request):
    try:
        data = await request.multipart()
        d = await data.next()
        with open(os.path.join(BaseConfig.STATIC_DIR + '/group_avatar/' + d.filename), 'wb') as f:
            chunk = await d.read_chunk()
            f.write(chunk)
    except:
        return json_response({'image_id': None})
    pool = request.app['pool']
    async with pool.acquire() as conn:
        image_id = await Images.create_image(path=d.filename, image_type='group', conn=conn)
    return json_response({'image_id': image_id})


async def remove_image(request):
    data = await request.json()
    image_id = data['avatar']['response']['image_id']
    pool = request.app['pool']
    async with pool.acquire() as conn:
        pathname = await Images.remove_image(image_id=image_id, conn=conn)
    is_removed = False
    os.remove(BaseConfig.STATIC_DIR + '/' + pathname['directory'] + '/' + pathname['href'])
    if os.path.exists(BaseConfig.STATIC_DIR + '/' + pathname['directory'] + '/' + pathname['href']) is False:
        is_removed = True
    return json_response({'response': is_removed})


class Signup(web.View):

    @aiohttp_jinja2.template('signup.html')
    async def get(self):
        return dict()

    async def post(self):
        data = await self.post()
        if data['email']:
            None
        else:
            data['email'] = 'None'
        if data['phone']:
            None
        else:
            data['phone'] = 'None'
        token = hashlib.sha256(data['user_name'].encode('utf8')).hexdigest()
        result = await UserCreate.create_user(data=data, token=token)
        if not result:
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)
        message = Parser(policy=default).parsestr(
            f'From: Achievements     <{BaseConfig.email_mail}>\n'
            f'To: <{data["email"]}>\n'
            'Subject: Activation account\n'
            '\n'
            f"http://localhost:8080/verify/{token}\n")
        smtp_server = SMTP_SSL(BaseConfig.smtp_server, port=BaseConfig.email_port)
        smtp_server.login(BaseConfig.email_mail, BaseConfig.email_password)
        smtp_server.sendmail(BaseConfig.email_mail, data['email'], message.as_string())
        smtp_server.quit()

        location = self.app.router['verify'].url_for()
        return web.HTTPFound(location=location)


class Verify(web.View):

    @aiohttp_jinja2.template('verify.html')
    async def get(self):
        location = str(self).split('/verify/')[-1][:-2]
        result = await UserVerifyAvatar.verify_user(href=location)
        if result:
            web.HTTPForbidden()
        return dict()


class NeedVerify(web.View):

    @aiohttp_jinja2.template('need_verify.html')
    async def get(self):
        return dict()


class Logout(web.View):

    async def get(self):
        session = await get_session(self)
        del session['user']
        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)
