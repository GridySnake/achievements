import React, {useState, useEffect} from "react";
import {Avatar, Button, Card, Col, Image, List, Skeleton, Tabs, Typography} from "antd";
import {GetAnyUserInfo} from "../../api/GeneralApi";
import StaticAvatars from "../StaticRoutes";

const {Title} = Typography;
const { Meta } = Card;
const { TabPane } = Tabs;

const CommunitiesContainer = () => {
    const [Communities, setCommunities] = useState(null);
    const url = '/communities'

    useEffect(() => {
        const  CommunitiesInfo = (Community) => {
            setCommunities(Community.communities)
        }
        GetAnyUserInfo(CommunitiesInfo, url)
    }, [url])

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
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                    description={item.sphere_name}
                                />
                                {/*<Button type="primary" htmlType="button" onClick={() => Unfollow(item.user_id)}>Unfollow</Button>*/}
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