import React, {useState, useEffect} from "react";
import { Image, Card, Typography, Statistic, Row, Col, Tooltip } from "antd";
import { LikeOutlined, DislikeOutlined, CheckCircleOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons';
import GetPersonalPageInfo from "../../api/Api";
import StaticAvatars from "../StaticRoutes";
import AvatarsContainer from "./AvatarsContainer";

const {Title} = Typography;

const PersonalPageContainer = () => {

    const [PersonalPage, setPersonalPage] = useState(null);
    const [visible, setVisible] = useState(false);
    // const [Avatar, setAvatar] = useState(null);

    console.log(PersonalPage)
    useEffect(() => {
        GetPersonalPageInfo(setPersonalPage)
    }, [setPersonalPage])

     // useEffect(() => {
     //     console.log(Avatar)
     //     AvatarsContainer({'User': PersonalPage.user, 'visible': visible}, setVisible, setAvatar)
     // }, [setVisible, setAvatar])

    const CardReturn = (post) => {
        if (post.href) {
            return <Image src={StaticAvatars.StaticPosts + post.href}/>;
        } else {
            return <></>;
        }}


    return (
        PersonalPage ?
            <div>
                <Col span={12}>
                    <Title level={2}>{PersonalPage.user.name + ' ' + PersonalPage.user.surname}</Title>
                    <Title level={2}>{PersonalPage.user.birthday}</Title>
                </Col>
                <Row>
                    <Col span={12}>
                        <AvatarsContainer user={PersonalPage.user} visible={visible} setVisible={setVisible} />
                        {/*{Avatar}*/}
                        {/*<Image*/}
                        {/*    preview={{visible: false}}*/}
                        {/*    width={200}*/}
                        {/*    src={StaticAvatars.StaticAvatars + PersonalPage.user.href[0]}*/}
                        {/*    onClick={() => setVisible(true)}*/}
                        {/*/>*/}
                        {/*<div style={{ display: 'none' }}>*/}
                        {/*    <Image.PreviewGroup preview={{ visible, onVisibleChange: vis => setVisible(vis) }}>*/}
                        {/*    {PersonalPage.user.href.map((avatar) => {*/}
                        {/*        return <Image src={StaticAvatars.StaticAvatars + avatar}/>*/}
                        {/*    })}*/}
                        {/*    </Image.PreviewGroup>*/}
                        {/*</div>*/}
                    </Col>
                    <Col span={12}>
                        <Row>
                            <Tooltip title='Likes'>
                                <Statistic value={PersonalPage.statistics.likes} prefix={<LikeOutlined />} />
                            </Tooltip>
                            <Tooltip title='Dislikes'>
                                <Statistic value={PersonalPage.statistics.dislikes} prefix={<DislikeOutlined />} />
                            </Tooltip>
                            <Tooltip title='Recommendations'>
                                <Statistic value={PersonalPage.statistics.recommendations} prefix={<CheckCircleOutlined />} />
                            </Tooltip>
                            <Tooltip title='Followers'>
                                <Statistic value={PersonalPage.statistics.followers} prefix={<TeamOutlined />} />
                            </Tooltip>
                            <Tooltip title='Followings'>
                                <Statistic value={PersonalPage.statistics.followings} prefix={<UserOutlined />} />
                            </Tooltip>
                        </Row>
                    </Col>
                </Row>
                <Title level={3}>{PersonalPage.user.bio}</Title>
                <div>
                {PersonalPage.posts.map((post) => {
                    return(
                    <Card title={post.date_created} style={{ width: 300 }}>
                        <p>{post.message}</p>
                        {CardReturn(post)}
                    </Card>)
                })}
                    </div>
            </div>
         :
            <></>
    )
}

export default PersonalPageContainer