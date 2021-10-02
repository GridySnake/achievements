import hashlib
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from models.user import User
from models.post import Post
from config.common import BaseConfig
from email.message import EmailMessage
import smtplib
import ssl
from aiosmtplib import send


class Login(web.View):

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        return dict()

    async def post(self):
        data = await self.post()
        if '@' in data['email']:
            type = 'email'
        else:
            type = 'phone'
        user = await User.get_user_by_email_phone(email=data['email'], type=type)
        if user.get('error'):
            return web.HTTPNotFound()

        if user['password'] == hashlib.sha256(data['password'].encode('utf8')).hexdigest():
            session = await get_session(self)
            session['user'] = user
            location = str(f"/{session['user']['id']}")
            return web.HTTPFound(location=location)

        return web.HTTPNotFound()


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
        result = await User.create_new_user(data=data)
        if not result:
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)
        message = EmailMessage()
        message["From"] = BaseConfig.email_mail
        message["To"] = data['email']
        message["Subject"] = "Hello World!"
        message.set_content("Sent via aiosmtplib")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(BaseConfig.smtp_server, BaseConfig.email_port, context=context) as server:
            #server.ehlo()
            #server.starttls(context=context)
            #server.ehlo()
            server.login(BaseConfig.email_user, BaseConfig.email_password)
            server.sendmail(BaseConfig.email_mail, data['email'], message)
        # await send(
        #         message,
        #         hostname=BaseConfig.smtp_server,
        #         port=BaseConfig.port,
        #         username=BaseConfig.email_user,
        #         password=BaseConfig.email_password,
        #         start_tls=True, tls_context=context
        #     )

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)


class Logout(web.View):

    async def get(self):
        session = await get_session(self)
        del session['user']
        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)


class PostView(web.View):

    async def post(self):
        data = await self.post()
        session = await get_session(self)
        if 'user' in session and data['message']:
            await Post.create_post(user_id=session['user']['id'], message=data['message'])
            return web.HTTPFound(location=self.app.router['index'].url_for())

        return web.HTTPForbidden()
