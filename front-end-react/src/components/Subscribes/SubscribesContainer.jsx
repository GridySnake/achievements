import React, {useEffect, useState} from "react";
import {CreateUserChat, GetAnyInfo} from "../../api/GeneralApi";
import {Avatar, Button, List, Skeleton, Tabs} from "antd";
import StaticAvatars from "../StaticRoutes";
import makeAction from "../../api/PageActions";
import {useNavigate} from "react-router";

const { TabPane } = Tabs;

const SubscribesContainer = () => {
    const [Friends, setFriends] = useState(null);
    const [Followers, setFollowers] = useState(null);
    const [Followings, setFollowings] = useState(null);
    const [Blocked, setBlocked] = useState(null);
    const [Suggestions, setSuggestions] = useState(null);
    const navigate = useNavigate();
    const url = '/subscribes'

    useEffect(() => {
        const setInfoSubscribes = (Subscribes) => {
            setFriends(Subscribes.friends)
            setFollowers(Subscribes.followers)
            setFollowings(Subscribes.followings)
            setBlocked(Subscribes.blocked)
            setSuggestions(Subscribes.suggestions)
        }
        GetAnyInfo(setInfoSubscribes, url)
    }, [url])

    const Unfollow = (user_id) => {
        makeAction('/unfollow', {'user_passive_id': user_id}, (value) => {
            setFriends(value[0])
            setFollowers(value[1])
        })
    }
    const Follow = (user_id) => {
        makeAction('/follow', {'user_passive_id': user_id}, (value) => {
            setFriends(value[0])
            setFollowers(value[1])
            setFollowings(value[2])
        })
    }
    const Block = (user_id) => {
        makeAction('/block', {'user_passive_id': user_id}, (value) => {
            setFriends(value[0])
            setFollowers(value[1])
            setFollowings(value[2])
            setBlocked(value[3])
        })
    }
    const Unblock = (user_id) => {
        makeAction('/unblock', {'user_passive_id': user_id}, (value) => {
            setFriends(value[0])
            setFollowers(value[1])
            setFollowings(value[2])
            setBlocked(value[3])
        })
    }

    const Chat = (item) => {
        if (item.chat_id !== null) {
            navigate(`/chat/${item.chat_id}`)
        } else {
            CreateUserChat({'user_id': item.user_id}, (chat_id) => {
                navigate(`/chat/${chat_id}`)
            })
        }
    }

    return (
        Suggestions?
        <Tabs defaultActiveKey="Suggestions">
            <TabPane tab="Suggestions" key="Suggestions">
                <List
                    itemLayout="horizontal"
                    dataSource={Suggestions}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.bio}
                                />
                                <Button type="primary" htmlType="button" onClick={() => Follow(item.user_id)}>Follow</Button>
                                <Button type="primary" htmlType="button" onClick={() => Block(item.user_id)}>Block</Button>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Friends" key="Friends">
                <List
                    itemLayout="horizontal"
                    dataSource={Friends}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.bio}
                                />
                                <Button type="primary" htmlType="button" onClick={() => Chat(item)}>Chat</Button>
                                <Button type="primary" htmlType="button" onClick={() => Unfollow(item.user_id)}>Unfollow</Button>
                                <Button type="primary" htmlType="button" onClick={() => Block(item.user_id)}>Block</Button>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Followers" key="Followers">
                <List
                    itemLayout="horizontal"
                    dataSource={Followers}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.bio}
                                />
                                <Button type="primary" htmlType="button" onClick={() => Follow(item.user_id)}>Follow</Button>
                                <Button  type="primary" htmlType="button" onClick={() => Block(item.user_id)}>Block</Button>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Followings" key="Followings">
                <List
                    itemLayout="horizontal"
                    dataSource={Followings}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.bio}
                                />
                                <Button type="primary" htmlType="button" onClick={() => Unfollow(item.user_id)}>Unfollow</Button>
                                <Button type="primary" htmlType="button" onClick={() => Block(item.user_id)}>Block</Button>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Blocked" key="Blocked">
                <List
                    itemLayout="horizontal"
                    dataSource={Blocked}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.bio}
                                />
                                <Button  type="primary" htmlType="button" onClick={() => Unblock(item.user_id)}>Unblock</Button>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
        </Tabs>
            : <></>
    )
}


export default SubscribesContainer;