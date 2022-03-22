import React, {useState, useEffect } from "react";
import { Image, Card, Typography, Row, Col, Button } from "antd";
import { LikeOutlined, DislikeOutlined, CheckCircleOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons';
import GetPersonalPageInfo from "../../api/Api";
import StaticAvatars from "../StaticRoutes";
import AvatarsContainer from "./AvatarsContainer";
import { useParams, useLocation } from 'react-router-dom'
import makeAction from "../../api/PageActions";

const {Title} = Typography;

const PersonalPageContainer = () => {
    const [PersonalPage, setPersonalPage] = useState(null);
    const [likeColor, setLikeColor] = useState(null);
    const [like, setLike] = useState(null);
    const [dislike, setDislike] = useState(null);
    const [recommend, setRecommend] = useState(null);
    const [dislikeColor, setDislikeColor] = useState(null);
    const [recommendColor, setRecommendColor] = useState(null);
    const [likes, setLikes] = useState(null);
    const [dislikes, setDislikes] = useState(null);
    const [recommends, setRecommends] = useState(null);
    const [followers, setFollowers] = useState(null);
    const [followings, setFollowings] = useState(null);
    const {id} = useParams();
    const {pathname} = useLocation();
    const [pEvent, setpEvent] = useState(null);

    useEffect(() => {
        const fillUserInfo = (PersonalPage) => {
            setPersonalPage(PersonalPage)
            setLike(PersonalPage.actions[0])
            setDislike(PersonalPage.actions[1])
            setRecommend(PersonalPage.actions[2])
            setLikeColor(color(PersonalPage.actions[0]))
            setDislikeColor(color(PersonalPage.actions[1]))
            setRecommendColor(color(PersonalPage.actions[2]))
            setLikes(PersonalPage.statistics.likes)
            setDislikes(PersonalPage.statistics.dislikes)
            setRecommends(PersonalPage.statistics.recommendations)
            setFollowers(PersonalPage.statistics.followers)
            setFollowings(PersonalPage.statistics.followings)
            setpEvent(pointEvent(PersonalPage.myPage))
        }
        GetPersonalPageInfo(fillUserInfo, id)
    }, [id])

    const CardReturn = (post) => {
        if (post.href) {
            return <Image src={StaticAvatars.StaticPosts + post.href}/>;
        } else {
            return <></>;
        }}

    const color = (bool) => {
        if (bool) {
            return "#ee004b"
        } else {
            return "#00ee00"
        }
    }

    const pointEvent = (bool) => {
        if (bool) {
            return "none"
        } else {
            return "auto"
        }
    }

    const MakeLike = () => {
        if (like) {
            makeAction('/unlike', {owner_id: id, owner_type: pathname.split('/')[1]}, (value)=> {
                setLike(false)
                setLikeColor("#00ee00")
                setLikes(value)
            })

        } else {
            makeAction('/like', {owner_id: id, owner_type: pathname.split('/')[1]}, (value) => {
                setLike(true)
                setLikeColor("#ee004b")
                setLikes(value)
            })
        }
    }

    const MakeDislike = () => {
        if (dislike) {
            makeAction('/undislike', {owner_id: id, owner_type: pathname.split('/')[1]}, (value) => {
                setDislike(false)
                setDislikeColor("#00ee00")
                setDislikes(value)
            })
        } else {
            makeAction('/dislike', {owner_id: id, owner_type: pathname.split('/')[1]}, (value) => {
                setDislike(true)
                setDislikeColor("#ee004b")
                setDislikes(value)
            })
        }
    }

    const MakeRecommend = () => {
        if (recommend) {
            makeAction('/unrecommend', {owner_id: id, owner_type: pathname.split('/')[1]}, (value) => {
                setRecommend(false)
                setRecommendColor("#00ee00")
                setRecommends(value)
            })
        } else {
            makeAction('/recommend', {owner_id: id, owner_type: pathname.split('/')[1]}, (value) => {
                setRecommend(true)
                setRecommendColor("#ee004b")
                setRecommends(value)
            })

        }
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
                        <AvatarsContainer user={PersonalPage.user} />
                    </Col>
                    <Col span={12}>
                        <Row>
                            <Button type="primary" htmlType="button" onClick={MakeLike} style={{background: likeColor,
                                pointerEvents: pEvent}}
                                    icon={<LikeOutlined />} title="Likes">
                                {likes}
                            </Button>
                            <Button type="primary" htmlType="button" onClick={MakeDislike} title="Dislikes"
                                    style={{background: dislikeColor, pointerEvents: pEvent}} icon={<DislikeOutlined />}>
                                {dislikes}
                            </Button>
                            <Button type="primary" htmlType="button" onClick={MakeRecommend} title="Recommendations"
                                    style={{background: recommendColor, pointerEvents: pEvent}} icon={<CheckCircleOutlined />}>
                                {recommends}
                            </Button>
                            <Button type="primary" title="Followers" style={{pointerEvents: "none"}} icon={<TeamOutlined />}>
                                {followers}
                            </Button>
                            <Button type="primary" title="Followings" style={{pointerEvents: "none"}} icon={<UserOutlined />}>
                                {followings}
                            </Button>
                            {/*<Button type="primary" htmlType="button" onClick={MakeDislike}>*/}
                            {/*    <StatisticContainer title='Dislikes' values={PersonalPage.statistics.dislikes}*/}
                            {/*                    icon={<DislikeOutlined />} action={PersonalPage.actions}*/}
                            {/*                    color={dislikeColor} setDislikeColor={setDislikeColor}*/}
                            {/*                    setDislike={setDislike} />*/}
                            {/*</Button>*/}
                            {/*<Button type="primary" htmlType="button" onClick={MakeRecommend}>*/}
                            {/*    <StatisticContainer title='Recommendations'  setRecommend={setRecommend}*/}
                            {/*                    values={PersonalPage.statistics.recommendations}*/}
                            {/*                    icon={<CheckCircleOutlined />} action={PersonalPage.actions}*/}
                            {/*                    color={recommendColor} setRecommendColor={setRecommendColor}/>*/}
                            {/*</Button>*/}
                            {/*<StatisticContainer title='Followers' values={PersonalPage.statistics.followers}*/}
                            {/*                    icon={<TeamOutlined />} />*/}
                            {/*<StatisticContainer title='Followings' values={PersonalPage.statistics.followings}*/}
                            {/*                    icon={<UserOutlined />} />*/}
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