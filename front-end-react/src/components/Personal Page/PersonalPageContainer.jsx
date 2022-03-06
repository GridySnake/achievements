import React, {useState, useEffect} from "react";
import { Image, Card, Typography, Statistic, Row, Col, Tooltip } from "antd";
import { LikeOutlined, DislikeOutlined, CheckCircleOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons';
import GetPersonalPageInfo from "../../api/Api";
import StaticAvatars from "../StaticRoutes";
import AvatarsContainer from "./AvatarsContainer";
import { useParams } from 'react-router-dom'

const {Title} = Typography;

const PersonalPageContainer = () => {

    const [PersonalPage, setPersonalPage] = useState(null);
    const [visible, setVisible] = useState(false);
    const [likeColor, setLikeColor] = useState("#ee004b");
    const [dislikeColor, setDislikeColor] = useState("#ee004b");
    const [recommendColor, setRecommendColor] = useState("#ee004b");
    const {id} = useParams();



    console.log(PersonalPage)
    useEffect(() => {
        GetPersonalPageInfo(setPersonalPage, id)
    }, [setPersonalPage, id])

    const CardReturn = (post) => {
        if (post.href) {
            return <Image src={StaticAvatars.StaticPosts + post.href}/>;
        } else {
            return <></>;
        }}

    const Actions = (title, values, icon, action, color) => {
        console.log(action)
    try {
        if (PersonalPage.actions[0]) {
            setLikeColor("#00ee00")
        }
        if (PersonalPage.actions[1]) {
            setDislikeColor("#00ee00")
        }
        if (PersonalPage.actions[1]) {
            setRecommendColor("#00ee00")
        }
    } catch (e) {
            console.log(e)
    }
    return (
        <div>
        <Tooltip title={title}>
            <Statistic value={values} prefix={icon}
                       style={{background: color}} />
        </Tooltip>
            </div>
    )
    }


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
                    </Col>
                    <Col span={12}>
                        <Row>
                            <Actions title='Likes' values={PersonalPage.statistics.likes} icon={<LikeOutlined />}
                                     action={PersonalPage.actions} color={likeColor} />
                            <Tooltip title='Likes'>
                                <Statistic value={PersonalPage.statistics.likes} prefix={<LikeOutlined />}
                                           style={{background: likeColor}} />
                            </Tooltip>
                            <Tooltip title='Dislikes'>
                                <Statistic value={PersonalPage.statistics.dislikes} prefix={<DislikeOutlined />}
                                           style={{background: dislikeColor}} />
                            </Tooltip>
                            <Tooltip title='Recommendations'>
                                <Statistic value={PersonalPage.statistics.recommendations} prefix={<CheckCircleOutlined />}
                                           style={{background: recommendColor}} />
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