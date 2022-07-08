import React, {useState, useEffect} from "react";
import {Avatar, Button, Card, Col, Descriptions, Image, List, Skeleton, Tabs, Typography, Popover } from "antd";
import {GetAnyInfo} from "../../api/GeneralApi";
import StaticAvatars from "../StaticRoutes";
import {useLocation, useParams} from "react-router-dom";
import {UserOutlined} from "@ant-design/icons";

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
    const {id} = useParams();
    const {pathname} = useLocation();
    const url = `/course/${id}`

    useEffect(() => {
        const  CourseInfo = (Course) => {
            setGoals(Course.goals)
            setOwner(Course.owner)
            setParticipants(Course.participants)
            if (owner) {
                setSubscribers(Course.subscribers)
            }
            setConditions(Course.conditions)
            setInCourse(Course.in_course)
            setCourse(Course.course)
        }
        GetAnyInfo(CourseInfo, url)
    }, [url])

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
                        return(<a href={'/user/' + participant.user_id}><p>{participant.name + ' ' + participant.surname}</p></a>)
                    })
                    } title="Participants" trigger="click">
                    <Button type="primary" title="Participants" icon={<UserOutlined />} >
                        {course.joined}
                    </Button>
                </Popover>
            </>
            :
            <></>
    )
};
export default CourseContainer;