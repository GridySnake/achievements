import React, {useEffect, useState} from "react";
import GetAnyInfo from "../../api/GeneralApi";
import {Avatar, List, Skeleton, Tabs} from "antd";
import StaticAvatars from "../StaticRoutes";

const { TabPane } = Tabs;

function callback(key) {
  console.log(key);
}

const SubscribesContainer = () => {
    const [Subscribes, setSubscribes] = useState(null);
    useEffect(() => {
        GetAnyInfo(setSubscribes, '/subscribes')
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