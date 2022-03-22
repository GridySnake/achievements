import React, {useEffect, useState} from "react";
import {GetAnyUserInfo} from "../../api/GeneralApi";
import {Avatar, List, Card, Tabs} from "antd";
import StaticAvatars from "../StaticRoutes";
import {useNavigate} from "react-router";

const { TabPane } = Tabs;

const ChatsContainer = () => {
    const [Users, setUsers] = useState(null);
    const [Groups, setGroups] = useState(null);
    const [Communities, setCommunities] = useState(null);
    const [Courses, setCourses] = useState(null);
    const navigate = useNavigate();
    const url = '/messages'

    useEffect(() => {
        const setInfoChats = (Chats) => {
            setUsers(Chats.users)
            setGroups(Chats.groups)
            setCommunities(Chats.followings)
            setCourses(Chats.blocked)
        }
        GetAnyUserInfo(setInfoChats, url)
    }, [url])

    const toChat = (id) => {
        navigate(`/chat/${id}`)
    }

    const Message = (message) => {
        message = message.message
        if (message.chat_type === 0) {
            if (message.name === message.m_name && message.surname === message.m_surname) {
                var me = ''
            } else {
                var me = 'You: '
            }
            return (
                message.message?
                <div>
                    <p>{me + ' ' + message.message + ' ' + message.datetime}</p>
                </div>
                    : <></>
            )
        } else if (message.chat_type === 1) {
            return (
                message.message?
                <div>
                    <p>{message.m_name + ' ' + message.m_surname}</p>
                    <p>{message.message + ' ' + message.datetime}</p>
                </div>
                    : <></>
            )
        }
        else {
            console.log(1)
            return (
                <></>
            )
        }

        // return (
        //     message.message?
        //     <div>
        //         message.message
        //         message.datetime
        //         message.
        //         message.
        //     </div>
        //         : <></>
        // )
    }

    return (
        Users?
        <Tabs defaultActiveKey="Direct">
            <TabPane tab="Direct chats" key="Direct">
                <List
                    itemLayout="horizontal"
                    dataSource={Users}
                    renderItem={item =>
                            <Card onClick={() => toChat(item.chat_id)}>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                />
                                <Message message={item}/>
                            </Card>
                    }
                />
            </TabPane>
            <TabPane tab="Group chats" key="Groups">
                <List
                    itemLayout="horizontal"
                    dataSource={Groups}
                    renderItem={item => (
                        <Card onClick={() => toChat(item.chat_id)}>
                            <List.Item.Meta
                                avatar={<Avatar src={StaticAvatars.StaticGroupAvatars + item.href}/>}
                                title={<a href={'/chat/' + item.chat_id}>{item.group_name}</a>}
                            />
                            <Message message={item}/>
                        </Card>
                    )}
                />
            </TabPane>
            <TabPane tab="Community chats" key="Communities">
                <List
                    itemLayout="horizontal"
                    dataSource={Communities}
                    renderItem={item => (
                        <Card onClick={() => toChat(item.chat_id)}>
                            <List.Item.Meta
                                avatar={<Avatar src={StaticAvatars.StaticCommunityAvatars + item.href}/>}
                                title={<a href={'/community/' + item.community_id}>{item.community_name}</a>}
                            />
                            <Message message={item}/>
                        </Card>
                    )}
                />
            </TabPane>
            <TabPane tab="Course chats" key="Courses">
                <List
                    itemLayout="horizontal"
                    dataSource={Courses}
                    renderItem={item => (
                        <Card onClick={() => toChat(item.chat_id)}>
                            <List.Item.Meta
                                avatar={<Avatar src={StaticAvatars.StaticCourseAvatars + item.href}/>}
                                title={<a href={'/course/' + item.course_id}>{item.course_name}</a>}
                            />
                            <Message message={item}/>
                        </Card>
                    )}
                />
            </TabPane>
        </Tabs>
            : <></>
    )
}


export default ChatsContainer;