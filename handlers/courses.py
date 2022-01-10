import aiohttp_jinja2
from aiohttp import web
from models.course import *


class CoursesView(web.View):

    @aiohttp_jinja2.template('courses.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPFound(location=self.app.router['login'].url_for())

        courses = await CoursesGetInfo.get_user_course_suggestions(user_id=self.session['user']['id'])
        my_courses = await CoursesGetInfo.get_user_courses(user_id=self.session['user']['id'])
        return dict(courses=courses, my_courses=my_courses)


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
