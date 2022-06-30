import React, {useState, useEffect} from "react";
import {Avatar, Button, Card, Col, Image, List, Skeleton, Tabs, Typography} from "antd";
import {GetAnyInfo} from "../../api/GeneralApi";
import StaticAvatars from "../StaticRoutes";

const {Title} = Typography;
const { Meta } = Card;
const { TabPane } = Tabs;

const CoursesContainer = () => {
    const [courses, setCourses] = useState(null);
    const [ownCourses, setOwnCourses] = useState(null);
    const [assistantCourses, setAssistantCourses] = useState(null);
    const [progressCourses, setProgressCourses] = useState(null);
    const [completeCourses, setCompleteCourses] = useState(null);

    const url = '/courses'

    useEffect(() => {
        const  CoursesInfo = (Course) => {
            setCourses(Course.sug_courses)
            setOwnCourses(Course.own_courses)
            setAssistantCourses(Course.assistant_courses)
            setProgressCourses(Course.progress)
            setCompleteCourses(Course.complete)
        }
        GetAnyInfo(CoursesInfo, url)
    }, [url])

    return (
        courses ?
        <Tabs defaultActiveKey="Suggestions">
            <TabPane tab="Suggestions" key="Suggestions">
                <List
                    itemLayout="horizontal"
                    dataSource={courses}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticCourseAvatars + item.href}/>}
                                    title={<a href={'/course/' + item.course_id}>{item.course_name}</a>}
                                    description={item.sphere_name}
                                />
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="In Progress" key="In Progress">
                <List
                    itemLayout="horizontal"
                    dataSource={progressCourses}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticCourseAvatars + item.href}/>}
                                    title={<a href={'/course/' + item.course_id}>{item.course_name}</a>}
                                    description={item.sphere_name}
                                />
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Completed" key="Completed">
                <List
                    itemLayout="horizontal"
                    dataSource={completeCourses}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticCourseAvatars + item.href}/>}
                                    title={<a href={'/course/' + item.course_id}>{item.course_name}</a>}
                                    description={item.sphere_name}
                                />
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Owned" key="Owned">
                <List
                    itemLayout="horizontal"
                    dataSource={ownCourses}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticCourseAvatars + item.href}/>}
                                    title={<a href={'/course/' + item.course_id}>{item.course_name}</a>}
                                    description={item.sphere_name}
                                />
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Assistant" key="Assistant">
                <List
                    itemLayout="horizontal"
                    dataSource={assistantCourses}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticCourseAvatars + item.href}/>}
                                    title={<a href={'/course/' + item.course_id}>{item.course_name}</a>}
                                    description={item.sphere_name}
                                />
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
        </Tabs>:
            <></>
    )
};
export default CoursesContainer;