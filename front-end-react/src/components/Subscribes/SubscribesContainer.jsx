import React, {useEffect, useState} from "react";
import GetAnyUserInfo from "../../api/GeneralApi";
import {Avatar, Button, List, Skeleton, Tabs} from "antd";
import StaticAvatars from "../StaticRoutes";
import makeAction from "../../api/PageActions";

const { TabPane } = Tabs;

function callback(key) {
  console.log(key);
}

const Unfollow = (user_id) => {
    makeAction('/unfollow', {'user_passive_id': user_id})
}
const Follow = (user_id) => {
    makeAction('/follow', {'user_passive_id': user_id})
}
const Block = (user_id) => {
    makeAction('/block', {'user_passive_id': user_id})
}
const Unblock = (user_id) => {
    makeAction('/unblock', {'user_passive_id': user_id})
}

const SubscribesContainer = () => {
    const [Subscribes, setSubscribes] = useState(null);
    useEffect(() => {
        GetAnyUserInfo(setSubscribes, '/subscribes')
    }, [setSubscribes])
    console.log(Subscribes)

    return (
        Subscribes?
        <Tabs defaultActiveKey="1" onChange={callback}>
            <TabPane tab="Friends" key="1">
                <List
                    itemLayout="horizontal"
                    dataSource={Subscribes.friends}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.bio}
                                />
                                <Button onClick={<Unfollow user_id={item.user_id}/>}>Unfollow</Button>
                                <Button onClick={<Block user_id={item.user_id}/>}>Block</Button>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Followers" key="2">
                <List
                    itemLayout="horizontal"
                    dataSource={Subscribes.followers}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.bio}
                                />
                                <Button onClick={<Follow user_id={item.user_id}/>}>Follow</Button>
                                <Button onClick={<Block user_id={item.user_id}/>}>Block</Button>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Followings" key="3">
                <List
                    itemLayout="horizontal"
                    dataSource={Subscribes.followings}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.bio}
                                />
                                <Button onClick={<Unfollow user_id={item.user_id}/>}>Unfollow</Button>
                                <Button onClick={<Block user_id={item.user_id}/>}>Block</Button>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Blocked" key="4">
                <List
                    itemLayout="horizontal"
                    dataSource={Subscribes.blocked}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.bio}
                                />
                                <Button onClick={<Unblock user_id={item.user_id}/>}>Unblock</Button>
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