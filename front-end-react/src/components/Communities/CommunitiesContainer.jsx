import React, {useState, useEffect} from "react";
import GetPersonalPageInfo from "../../api/Api";
import {Card, Col, Image, Typography} from "antd";
import GetAnyUserInfo from "../../api/GeneralApi";
import AvatarsContainer from "../Personal Page/AvatarsContainer";
import StaticAvatars from "../StaticRoutes";

const {Title} = Typography;
const { Meta } = Card;

const CommunitiesContainer = () => {
    const [CommunitiesPage, setCommunitiesPage] = useState(null);


    useEffect(() => {
        GetAnyUserInfo(setCommunitiesPage, '/communities')
    }, [setCommunitiesPage])

    const CardReturn = (post) => {
        if (post.href) {
            return <Image src={StaticAvatars.StaticCommunityAvatars + post.href}/>;
        } else {
            return <></>;
        }}

    return (
        CommunitiesPage ?
        <div>

            {CommunitiesPage.communities.map((community) => {
                    return(
                    <Card
                        span={12}>
                            {CardReturn(community)}
                            <Title level={2}>{community.community_name}</Title>
                            <Meta title= {'Sphere Name: ' + community.sphere_name}/>
                            <Meta title={'Subsphere Name: ' + community.subsphere_name}/>
                    </Card>)
                })}
        </div>:
            <></>
    )
};
export default CommunitiesContainer