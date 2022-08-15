import React, {useState, useEffect} from "react";
import {Avatar, Button, Card, Col, Image, List, Skeleton, Tabs, Typography} from "antd";
import {GetAnyInfo} from "../../api/GeneralApi";
import StaticAvatars from "../StaticRoutes";
import makeAction from "../../api/PageActions";
import {useNavigate} from "react-router";

const {Title} = Typography;
const { Meta } = Card;
const { TabPane } = Tabs;

const CommunitiesContainer = () => {
    const [Communities, setCommunities] = useState(null);
    const [OwnCommunities, setOwnCommunities] = useState(null);
    const [RecommendCommunities, setRecommendCommunities] = useState(null);
    const [change, setChange] = useState(null);
    const url = '/communities'

    const navigate = useNavigate();


    useEffect(() => {
        const  CommunitiesInfo = (Community) => {
            setCommunities(Community.communities)
            setOwnCommunities(Community.owner_communities)
            setRecommendCommunities(Community.communities_recommend)
        }
        GetAnyInfo(CommunitiesInfo, url)
    }, [url, change])


    const Join = (community_id) => {
        makeAction('/join_community', {'community_id': community_id}, (value) => {
                setChange(value)
            }
        )
    }

    const Leave = (community_id) => {
        makeAction('/leave_community', {'community_id': community_id}, (value) => {
                setChange(value)
            }
        )
    }
    // const Leave = (user_id) => {
    //     makeAction('/unfollow', {'user_passive_id': user_id}, (value) => {
    //         setFriends(value[0])
    //         setFollowers(value[1])
    //     })
        // }

// const CommunitiesContainer = () => {
//     const [CommunitiesPage, setCommunitiesPage] = useState(null);
//
//
//     useEffect(() => {
//         GetAnyUserInfo(setCommunitiesPage, '/communities')
//     }, [setCommunitiesPage])

    // const CardReturn = (post) => {
    //     if (post.href) {
    //         return <Image src={StaticAvatars.StaticCommunityAvatars + post.href}/>;
    //     } else {
    //         return <></>;
    //     }}

    // return (
    //     CommunitiesPage ?
    //     <div>
    //
    //         {CommunitiesPage.communities.map((community) => {
    //                 return(
    //                 <Card
    //                     span={12}>
    //                         {CardReturn(community)}
    //                         <Title level={2}>{community.community_name}</Title>
    //                         <Meta title= {'Sphere Name: ' + community.sphere_name}/>
    //                         <Meta title={'Subsphere Name: ' + community.subsphere_name}/>
    //                 </Card>)
    //             })}
    //     </div>:
    //         <></>
    // )
    return (
        Communities ?
        <Tabs defaultActiveKey="Communities">
            <TabPane tab="Communities" key="Communities">
                <List
                    itemLayout="horizontal"
                    dataSource={Communities}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticCommunityAvatars + item.href}/>}
                                    title={<a href={'/community/' + item.community_id}>{item.community_name}</a>}
                                    description={item.sphere_name}
                                />
                                <Button type="primary" htmlType="button" onClick={() => Leave(item.community_id)}>Leave</Button>
                                {/*<Button type="primary" htmlType="button" onClick={() => Block(item.user_id)}>Block</Button>*/}
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Created" key="Created">
                <List
                    itemLayout="horizontal"
                    dataSource={OwnCommunities}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticCommunityAvatars + item.href}/>}
                                    title={<a href={'/community/' + item.community_id}>{item.community_name}</a>}
                                    description={item.sphere_name}
                                />
                                {/*<Button type="primary" htmlType="button" onClick={() => Unfollow(item.community_id)}>Unfollow</Button>*/}
                                {/*<Button type="primary" htmlType="button" onClick={() => Block(item.user_id)}>Block</Button>*/}
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Suggestions" key="Suggestions">
                <List
                    itemLayout="horizontal"
                    dataSource={RecommendCommunities}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticCommunityAvatars + item.href}/>}
                                    title={<a href={'/community/' + item.community_id}>{item.community_name}</a>}
                                    description={item.sphere_name}
                                />
                                <Button type="primary" htmlType="button" onClick={() => Join(item.community_id)}>Join</Button>
                                {/*<Button type="primary" htmlType="button" onClick={() => Block(item.user_id)}>Block</Button>*/}
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
        </Tabs>:
            <></>
    )
};
export default CommunitiesContainer