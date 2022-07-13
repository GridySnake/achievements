import React, {useState, useEffect} from "react";
import {Avatar, Button, List, Skeleton, Tabs, Rate, Popconfirm, Form, Input, Radio, Select} from "antd";
import {GetAnyInfo, GetSubspheresBySphere, GetUsersByType} from "../../api/GeneralApi";
import StaticAvatars from "../StaticRoutes";
import makeAction from "../../api/PageActions";
import {Option} from "antd/es/mentions";
import type {RadioChangeEvent} from "antd";

const { TabPane } = Tabs;

const CoursesContainer = () => {
    const [courses, setCourses] = useState(null);
    const [ownCourses, setOwnCourses] = useState(null);
    const [assistantCourses, setAssistantCourses] = useState(null);
    const [progressCourses, setProgressCourses] = useState(null);
    const [completeCourses, setCompleteCourses] = useState(null);
    const [requests, setRequests] = useState(null);
    const [change, setChange] = useState(null);
    const [rate, setRate] = useState(null);
    const [courseName, setCourseName] = useState(null);
    const [courseDescription, setCourseDescription] = useState(null);
    const [spheres, setSpheres] = useState(null);
    const [subsphere, setSubsphere] = useState(null);
    const [subspheres, setSubspheres] = useState(null);
    const [sphere, setSphere] = useState(null);
    const [userType, setUserType] = useState(null);
    const [paymentType, setPaymentType] = useState(null);
    const [studyType, setStudyType] = useState(null);
    const [userId, setUserId] = useState(null);
    const [users, setUsers] = useState(null);
    const [price, setPrice] = useState(null);
    const [currencies, setCurrencies] = useState(null);
    const [currency, setCurrency] = useState(null);

    const url = '/courses'

    const avatarPath = {
        0: StaticAvatars.StaticAvatars, 1: StaticAvatars.StaticGroupAvatars,
        2: StaticAvatars.StaticCommunityAvatars, 3: StaticAvatars.StaticCourseAvatars
    }

    const radioOptionsUser = [
        {label: 'User', value: 0},
        {label: 'Community', value: 1}
    ];
    const radioOptionsPayment = [
        {label: 'Paid', value: 0},
        {label: 'Free', value: 1}
    ]
    const radioOptionsStudy = [
        {label: 'Offline', value: 0},
        {label: 'Online', value: 1}
    ]

    useEffect(() => {
        const CoursesInfo = (Course) => {
            setOwnCourses(Course.own_courses)
            setAssistantCourses(Course.assistant_courses)
            setProgressCourses(Course.progress)
            setCompleteCourses(Course.complete)
            setRequests(Course.requests)
            setSpheres(Course.create.spheres)
            setCurrencies(Course.create.currencies)
            setCourses(Course.sug_courses)
        }
        GetAnyInfo(CoursesInfo, url)
    }, [url, change])

    const Accept = (course_id) => {
        makeAction('/accept_invitation_course', {'course_id': course_id}, (value) => {
                setChange(value)
            }
        )
    }

    const Decline = (course_id) => {
        makeAction('/decline_invitation_course', {'course_id': course_id}, (value) => {
                setChange(value)
            }
        )
    }

    const Join = (course_id) => {
        makeAction('/join_course', {'course_id': course_id}, (value) => {
                setChange(value)
            }
        )
    }

    const Leave = (course_id) => {
        makeAction('/leave_course', {'course_id': course_id}, (value) => {
                setChange(value)
            }
        )
    }

    useEffect(() => {
        const GetSubspheres = (Subspheres) => {
            setSubspheres(Subspheres.subspheres)
        }
        GetSubspheresBySphere(sphere, GetSubspheres)
    }, [sphere])

    useEffect(() => {
        if (userType !== 0) {
            const GetUsersByTypes = (User) => {
                setUsers(User.users)
            }
            GetUsersByType(userType, GetUsersByTypes)
        } else {
            setUsers(null)
            setUserId(null)
        }
    }, [userType])

    const RadioChangeUser = ({target: {value}}: RadioChangeEvent) => {
        setUserType(value);
    };

    const RadioChangePayment = ({target: {value}}: RadioChangeEvent) => {
        setPaymentType(value);
    };

    const RadioChangeStudy = ({target: {value}}: RadioChangeEvent) => {
        setStudyType(value);
    };

    const CreateCourse = () => {
        console.log(courseName, courseDescription, userType, userId, sphere, subsphere, paymentType, price, currency, studyType)
    }

    const Delete = (course_id) => {

    }

    const Learn = () => {

    }
    console.log()

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
                                <Button  type="primary" htmlType="button" onClick={() => Join(item.course_id)}>Join</Button>
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
                                <Button  type="primary" htmlType="button" onClick={() => Learn(item.course_id)}>Learn</Button>
                                <Popconfirm
                                    title="Leave this course?"
                                    onConfirm={() => Leave(item.course_id)}
                                    okText="Leave"
                                    cancelText="Cancel"
                                  >
                                    <Button  type="primary" htmlType="button" style={{"background": "red"}}>Leave</Button>
                                </Popconfirm>
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
                                <Rate allowClear={false} defaultValue={0} style={{'background': "blue"}} onChange={e => setRate(e)}/>
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
            <TabPane tab="Requests" key="Requests">
                <List
                    itemLayout="horizontal"
                    dataSource={requests}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticCourseAvatars + item.href}/>}
                                    title={<a href={'/course/' + item.course_id}>{item.course_name}</a>}
                                    description={item.sphere_name}
                                />
                                <Button  type="primary" htmlType="button" style={{"background": "green"}} onClick={() => Accept(item.course_id)}>Accept</Button>
                                <Button  type="primary" htmlType="button" style={{"background": "red"}} onClick={() => Decline(item.course_id)}>Decline</Button>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Create" key="Create">
                <Form name="create course"
                      labelCol={{
                        span: 6,
                      }}
                      wrapperCol={{
                        span: 8,
                      }}>
                    <Form.Item
                        label="Course name"
                        name="course_name"
                        rules={[
                          {
                            required: true,
                            message: 'Course name is required',
                          },
                        ]}
                        onChange={e => setCourseName(e.target.value)}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label="Course description"
                        name="course_description"
                        rules={[
                          {
                            required: true,
                            message: 'Course description is required',
                          },
                        ]}
                        onChange={e => setCourseDescription(e.target.value)}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label="Course creator type"
                        name="course_creator_type"
                        rules={[
                          {
                            required: true,
                            message: 'Course creator type is required',
                          }
                        ]}>
                        <Radio.Group
                            options={radioOptionsUser}
                            onChange={RadioChangeUser}
                            value={null}
                            optionType="button"
                            buttonStyle="solid"
                          />
                    </Form.Item>
                    {users ?
                        <Form.Item
                            label="Course creator"
                            name="course_creator"
                            rules={[
                              {
                                required: true,
                                message: 'Course creator is required',
                              }
                            ]}>
                            <Select defaultValue={null} onChange={e => setUserId(e)}>
                                {users.map((user) => {
                                    return (
                                        <Option value={user.user_id}><Avatar src={avatarPath[userType+1] + user.href}/>
                                            {user.user_name}</Option>
                                    )
                                })
                                }
                            </Select>
                        </Form.Item>
                        :
                        <></>
                    }
                    <Form.Item
                        label="Course sphere"
                        name="course_sphere"
                        rules={[
                          {
                            required: true,
                            message: 'Course sphere is required',
                          }
                        ]}>
                        <Select defaultValue={null} onChange={e => setSphere(e)}>
                            {spheres.map((sphere) => {
                                return (
                                    <Option value={sphere.sphere_id}>{sphere.sphere_name}</Option>
                                )
                            })
                            }
                        </Select>
                    </Form.Item>
                    {subspheres?
                        <Form.Item
                            label="Course subsphere"
                            name="course_subsphere"
                            rules={[
                              {
                                required: true,
                                message: 'Course subsphere is required',
                              }
                            ]}>
                            <Select defaultValue={null} onChange={e => setSubsphere(e)}>
                                {subspheres.map((subsphere) => {
                                    return (
                                        <Option value={subsphere.subsphere_id}>{subsphere.subsphere_name}</Option>
                                    )
                                })
                                }
                            </Select>
                        </Form.Item>
                        :
                        <></>
                    }
                    <Form.Item
                        label="Course payment type"
                        name="course_payment_type"
                        rules={[
                          {
                            required: true,
                            message: 'Course payment type is required',
                          }
                        ]}>
                        <Radio.Group
                            options={radioOptionsPayment}
                            onChange={RadioChangePayment}
                            value={null}
                            optionType="button"
                            buttonStyle="solid"
                          />
                    </Form.Item>
                    {paymentType === 0?
                        <Form.Item label="Course price"
                        name="course_price"
                        rules={[
                          {
                            required: true,
                            message: 'Course price is required',
                          }
                        ]}  onChange={e => setPrice(e.target.value)}>
                            <Input addonAfter={
                                <Select defaultValue={null} className="select-after" onChange={e => setCurrency(e)}>
                                    {currencies.map((currency) => {
                                        return (
                                            <Option value={currency.currency_id}>{currency.currency_symbol}</Option>
                                        )
                                    })}
                                </Select>} defaultValue={null}/>
                        </Form.Item>
                        :
                        <></>
                    }
                    <Form.Item
                        label="Course study type"
                        name="course_study_type"
                        rules={[
                          {
                            required: true,
                            message: 'Course study type is required',
                          }
                        ]}>
                        <Radio.Group
                            options={radioOptionsStudy}
                            onChange={RadioChangeStudy}
                            value={null}
                            optionType="button"
                            buttonStyle="solid"
                          />
                    </Form.Item>
                    <Button type="primary" onClick={CreateCourse}>Create Course</Button>
                </Form>
            </TabPane>
        </Tabs>:
            <></>
    )
};
export default CoursesContainer;