import React, {useState, useEffect} from "react";
import {Avatar, Button, Card, Col, Descriptions, Image, List, Skeleton, Tabs, Typography, Popover, Select, Form} from "antd";
import {GetAnyInfo} from "../../api/GeneralApi";
import StaticAvatars from "../StaticRoutes";
import {useLocation, useParams} from "react-router-dom";
import {UserOutlined} from "@ant-design/icons";
import makeAction from "../../api/PageActions";
import {useNavigate} from "react-router";
const { Option } = Select;
const {Title} = Typography;
const { Meta } = Card;
const { TabPane } = Tabs;


const CourseContainer = () => {
    const [course, setCourse] = useState(null);
    const [owner, setOwner] = useState(null);
    const [goals, setGoals] = useState(null);
    const [participants, setParticipants] = useState(null);
    const [subscribers, setSubscribers] = useState(null);
    const [conditions, setConditions] = useState(null);
    const [inCourse, setInCourse] = useState(null);
    const [membersAdd, setMembersAdd] = useState(null);
    const [AddMembersAllow, setAddMembersAllow] = useState(null);
    const [change, setChange] = useState(null);
    const {id} = useParams();
    const {pathname} = useLocation();

    const url = `/course/${id}`

    const navigate = useNavigate();

    useEffect(() => {
        const  CourseInfo = (Course) => {
            setGoals(Course.goals)
            setOwner(Course.owner)
            setParticipants(Course.participants)
            if (Course.owner) {
                setSubscribers(Course.subscribers)
                if (Course.subscribers) {
                    setAddMembersAllow(true)
                }
            }
            setConditions(Course.conditions)
            setInCourse(Course.in_course)
            setCourse(Course.course)
        }
        GetAnyInfo(CourseInfo, url)
    }, [url, change])

    const CreatorName = () => {
        if (course.course_owner_type === 0) {
            return course.name + ' ' + course.surname
        } else if (course.course_owner_type === 1) {
            return course.community_name
        }
    }

    const CreatorLink = () => {
        if (course.course_owner_type === 0) {
            return '/user/'
        } else if (course.course_owner_type === 1) {
            return '/community/'
        }
    }

    const Learn = () => {
        navigate(`/study_course/${pathname.split('/')[2]}`)
    }

    const Join = () => {
        makeAction('/join_course', {'course_id': id}, (value) => {
            setChange(value)
        }
        )
    }

    const Leave = () => {
        makeAction('/leave_course', {'course_id': id}, (value) => {
            setChange(value)
        }
        )
    }

    const Add = () => {
        makeAction('/add_course_member', {'course_id': id, 'users': membersAdd}, (value) => {
            setChange(value)
        })
        setMembersAdd(null)
    }

    return (
        course ?
            <>
                <Descriptions title={course.course_name}>
                    <Descriptions.Item label="Description">{course.description}</Descriptions.Item>
                    <Descriptions.Item label="Creator"><a href={CreatorLink() + course.course_owner_id}>{CreatorName()}</a></Descriptions.Item>
                    <Descriptions.Item label="Language">{course.language_native}</Descriptions.Item>
                </Descriptions>
                <Popover content={
                    participants.map((participant) => {
                        return(<a href={'/user/' + participant.user_id} key={participant.user_id}><p key={participant.user_id}>{participant.name + ' ' + participant.surname}</p></a>)
                    })
                    } title="Participants" trigger="click">
                    <Button type="primary" title="Participants" icon={<UserOutlined />} >
                        {course.joined ?
                            course.joined
                            :
                            0
                        }
                    </Button>
                </Popover>
                {inCourse ?
                    <>
                        <Button type="primary" onClick={Learn}>Learn</Button>
                        <Button type="primary" onClick={Leave}>Leave</Button>
                    </>
                    :
                    <Button type="primary" onClick={Join}>Join</Button>
                }
                {AddMembersAllow ?
                    <Popover content={
                        <Form
                            labelCol={{
                                span: 6,
                            }}
                            wrapperCol={{
                                span: 8,
                            }}
                            initialValues={{
                                remember: false,
                            }}
                            autoComplete="off"
                        >
                            <Select
                               mode="multiple"
                               allowClear
                               style={{ width: '100%' }}
                               placeholder="Please select"
                               onChange={e => setMembersAdd(e)}
                            >
                                {subscribers.map((sub) => {
                                    return (<Option key={sub.user_id}>{sub.surname + ' ' + sub.name}</Option>)
                                })}
                            </Select>
                            <Button type="primary" onClick={() => Add()}>Add</Button>
                        </Form>

                        } title="Add participants" trigger="click">
                        <Button type="primary">Add members</Button>
                    </Popover>
                    :
                    <></>
                }
            </>
            :
            <></>
    )
};
export default CourseContainer;