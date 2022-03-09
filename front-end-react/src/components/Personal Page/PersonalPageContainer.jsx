import React, {useState, useEffect} from "react";
import { Image, Card, Typography, Row, Col, Button } from "antd";
import { LikeOutlined, DislikeOutlined, CheckCircleOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons';
import GetPersonalPageInfo from "../../api/Api";
import StaticAvatars from "../StaticRoutes";
import AvatarsContainer from "./AvatarsContainer";
import { useParams, useLocation } from 'react-router-dom'
import StatisticContainer from "./StatisticContainer";
import {makeAction} from "../../api/PageActions";

const {Title} = Typography;

const PersonalPageContainer = () => {

    const [PersonalPage, setPersonalPage] = useState(null);
    const [visible, setVisible] = useState(false);
    const [likeColor, setLikeColor] = useState("#ee004b");
    const [like, setLike] = useState(true);
    const [dislike, setDislike] = useState(true);
    const [recommend, setRecommend] = useState(true);
    const [dislikeColor, setDislikeColor] = useState("#ee004b");
    const [recommendColor, setRecommendColor] = useState("#ee004b");
    const {id} = useParams();
    const {pathname} = useLocation();



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

    const MakeLike = () => {
        if (!PersonalPage.myPage) {
            if (like) {
                makeAction('/unlike', {owner_id: id, owner_type: pathname.split('/')[1]})
            } else {
                makeAction('/like', {owner_id: id, owner_type: pathname.split('/')[1]})
            }
        }
    }
    const MakeDislike = () => {
        if (!PersonalPage.myPage) {
            if (dislike) {
                makeAction('/undislike', {owner_id: id, owner_type: pathname.split('/')[1]})
            } else {
                makeAction('/dislike', {owner_id: id, owner_type: pathname.split('/')[1]})
            }
        }
    }

    const MakeRecommend = () => {
        if (!PersonalPage.myPage) {
            if (recommend) {
                makeAction('/unrecommend', {owner_id: id, owner_type: pathname.split('/')[1]})
            } else {
                makeAction('/recommend', {owner_id: id, owner_type: pathname.split('/')[1]})
            }
        }
    }

    useEffect(() => {
        GetPersonalPageInfo(setPersonalPage, id)
    }, [setPersonalPage, id])
    // const generate = (action) => {
    //     if (action !== null) {
    //         console.log(1)
    //         return PersonalPage.actions
    //     } else {
    // const action = (action) => {
    //     if (action !== null) {
    //         console.log(1)
    //         return PersonalPage.actions
    //     } else {
    //         console.log(0)
    //         return null
    //     }
    // }}}

    // const valuesTooltips = [
    //     {
    //         title: 'Likes',
    //         values: PersonalPage.statistics.likes,
    //         icon: <LikeOutlined />,
    //         action: action(PersonalPage.actions),
    //         color: likeColor,
    //         setLikeColor: setLikeColor,
    //         setDislikeColor: null,
    //         setRecommendColor: null
    //     },
    //     {
    //         title: 'Dislikes',
    //         values: PersonalPage.statistics.dislikes,
    //         icon: <DislikeOutlined />,
    //         action: action(PersonalPage.actions),
    //         color: dislikeColor,
    //         setLikeColor: null,
    //         setDislikeColor: setDislikeColor,
    //         setRecommendColor: null
    //     },
    //     {
    //         title: 'Recommendations',
    //         values: PersonalPage.statistics.recommendations,
    //         icon: <CheckCircleOutlined />,
    //         action: action(PersonalPage.actions),
    //         color: recommendColor,
    //         setLikeColor: null,
    //         setDislikeColor: null,
    //         setRecommendColor: setRecommendColor
    //     },
    //     {
    //         title: 'Followers',
    //         values: PersonalPage.statistics.followers,
    //         icon: <TeamOutlined />,
    //         action: null,
    //         color: null,
    //         setLikeColor: null,
    //         setDislikeColor: null,
    //         setRecommendColor: null
    //     },
    //     {
    //         title: 'Followings',
    //         values: PersonalPage.statistics.followings,
    //         icon: <UserOutlined />,
    //         action: null,
    //         color: null,
    //         setLikeColor: null,
    //         setDislikeColor: null,
    //         setRecommendColor: null
    //     }]

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
                            {/*{valuesTooltips.map((tooltip, inx) => {*/}
                            <Button type="primary" htmlType="button" onClick={MakeLike}>
                                <StatisticContainer title='Likes' values={PersonalPage.statistics.likes}
                                                icon={<LikeOutlined />} action={PersonalPage.actions}
                                                color={likeColor} setLikeColor={setLikeColor} setLike={setLike} />
                            </Button>
                            <Button type="primary" htmlType="button" onClick={MakeDislike}>
                                <StatisticContainer title='Dislikes' values={PersonalPage.statistics.dislikes}
                                                icon={<DislikeOutlined />} action={PersonalPage.actions}
                                                color={dislikeColor} setDislikeColor={setDislikeColor}
                                                setDislike={setDislike} />
                            </Button>
                            <Button type="primary" htmlType="button" onClick={MakeRecommend}>
                                <StatisticContainer title='Recommendations'  setRecommend={setRecommend}
                                                values={PersonalPage.statistics.recommendations}
                                                icon={<CheckCircleOutlined />} action={PersonalPage.actions}
                                                color={recommendColor} setRecommendColor={setRecommendColor}/>
                            </Button>
                            <StatisticContainer title='Followers' values={PersonalPage.statistics.followers}
                                                icon={<TeamOutlined />} />
                            <StatisticContainer title='Followings' values={PersonalPage.statistics.followings}
                                                icon={<UserOutlined />} />
                            {/*<Tooltip title='Likes'>*/}
                            {/*    <Statistic value={PersonalPage.statistics.likes} prefix={<LikeOutlined />}*/}
                            {/*               style={{background: likeColor}} />*/}
                            {/*</Tooltip>*/}
                            {/*<Tooltip title='Dislikes'>*/}
                            {/*    <Statistic value={PersonalPage.statistics.dislikes} prefix={<DislikeOutlined />}*/}
                            {/*               style={{background: dislikeColor}} />*/}
                            {/*</Tooltip>*/}
                            {/*<Tooltip title='Recommendations'>*/}
                            {/*    <Statistic value={PersonalPage.statistics.recommendations} prefix={<CheckCircleOutlined />}*/}
                            {/*               style={{background: recommendColor}} />*/}
                            {/*</Tooltip>*/}
                            {/*<Tooltip title='Followers'>*/}
                            {/*    <Statistic value={PersonalPage.statistics.followers} prefix={<TeamOutlined />} />*/}
                            {/*</Tooltip>*/}
                            {/*<Tooltip title='Followings'>*/}
                            {/*    <Statistic value={PersonalPage.statistics.followings} prefix={<UserOutlined />} />*/}
                            {/*</Tooltip>*/}
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