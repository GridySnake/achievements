import aiohttp_jinja2
from aiohttp import web
from models.course import *
from models.information import InfoGet
from models.community import CommunityGetInfo
import os


class CoursesView(web.View):

    @aiohttp_jinja2.template('courses.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        own_courses = await CoursesGetInfo.get_own_courses(user_id=self.session['user']['id'])
        communities = await CommunityGetInfo.get_user_owner_communities(user_id=self.session['user']['id'])
        languages = await InfoGet.get_languages()
        courses = await CoursesGetInfo.get_user_course_suggestions(user_id=self.session['user']['id'])
        my_courses = await CoursesGetInfo.get_user_courses(user_id=self.session['user']['id'])
        return dict(courses=courses, my_courses=my_courses, languages=languages, communities=communities, own_courses=own_courses)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        data = await self.post()
        print(data['avatar'])
        avatar = data['avatar']
        data = dict(data)
        if 'online' in data.keys():
            data['online'] = True
        else:
            data['online'] = False
        if 'free' in data.keys():
            data['free'] = True
        else:
            data['free'] = False
        if 'as_community' in data.keys():
            data['type'] = 1
            user_id = data['community']
        else:
            data['type'] = 0
            user_id = self.session['user']['id']
        no_image = False
        if data['avatar'] == bytearray(b''):
            no_image = True
        else:
            with open(os.path.join(BaseConfig.STATIC_DIR + '/course_avatar/', avatar.filename), 'wb') as f:
                content = avatar.file.read()
                f.write(content)
            data['avatar'] = avatar.filename
        await CourseCreate.create_course(user_id=user_id, data=data, no_image=no_image)
        return web.HTTPFound(location='courses')


class CourseInfoView(web.View):

    @aiohttp_jinja2.template('course_info.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        location = str(self).split('/')[-1][:-2]
        course = await CoursesGetInfo.get_course_info(course_id=location)
        in_course = await CoursesGetInfo.is_user_in_course(course_id=location, user_id=self.session['user']['id'])
        return dict(course=course, in_course=in_course)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        course_id = str(self.__dict__['_message']).split('Referer')[-1].split(',')[1].split('course/')[1][:-2]
        data = await self.post()
        if 'join' in data.keys():
            await CoursesAction.join_course(course_id=course_id, user_id=self.session['user']['id'])
        else:
            await CoursesAction.leave_course(course_id=course_id, user_id=self.session['user']['id'])
        return web.HTTPFound(location='courses')


class CourseContent(web.View):
    @aiohttp_jinja2.template('course_content.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        course_id = str(self).split('/')[1]
        page = str(self).split('/course_content/')[-1][:-2]
        count = await CourseContent.count_course_content(course_id=course_id)
        page_content = await CourseContent.course_content_page(course_id=course_id, page=page)
        navigation = await CourseContent.course_content_navigation(course_id=course_id)
        return dict(count=count, page_content=page_content, navigation=navigation)
