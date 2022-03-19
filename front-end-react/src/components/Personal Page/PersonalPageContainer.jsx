import React, {useState, useEffect} from "react";
import { Image, Card, Typography, Row, Col, Button } from "antd";
import { LikeOutlined, DislikeOutlined, CheckCircleOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons';
import GetPersonalPageInfo from "../../api/Api";
import StaticAvatars from "../StaticRoutes";
import AvatarsContainer from "./AvatarsContainer";
import { useParams, useLocation } from 'react-router-dom'
import GetAnyUserInfo from "../../api/GeneralApi";
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

    const fillUserInfo = (PersonalPage) => {
        if (PersonalPage !== null) {
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
        }
    }

    useEffect(() => {
        GetPersonalPageInfo(fillUserInfo, id)
    }, [fillUserInfo, id])

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

    const MakeLike = () => {
        if (!PersonalPage.myPage) {
            if (like) {
                makeAction('/unlike', {owner_id: id, owner_type: pathname.split('/')[1]})
                setLike(false)
                setLikeColor("#00ee00")
                GetAnyUserInfo(setLikes, '/get_likes')
            } else {
                makeAction('/like', {owner_id: id, owner_type: pathname.split('/')[1]})
                setLike(true)
                setLikeColor("#ee004b")
                GetAnyUserInfo(setLikes, '/get_likes')
            }
        }
    }
    const MakeDislike = () => {
        if (!PersonalPage.myPage) {
            if (dislike) {
                makeAction('/undislike', {owner_id: id, owner_type: pathname.split('/')[1]})
                setDislike(false)
                setDislikeColor("#00ee00")
                GetAnyUserInfo(setDislikes, '/get_dislikes')
            } else {
                makeAction('/dislike', {owner_id: id, owner_type: pathname.split('/')[1]})
                setDislike(true)
                setDislikeColor("#ee004b")
                GetAnyUserInfo(setDislikes, '/get_dislikes')
            }
        }
    }

    const MakeRecommend = () => {
        if (!PersonalPage.myPage) {
            if (recommend) {
                makeAction('/unrecommend', {owner_id: id, owner_type: pathname.split('/')[1]})
                setRecommend(false)
                setRecommendColor("#00ee00")
                GetAnyUserInfo(setRecommends, '/get_recommendations')
            } else {
                setRecommends(makeAction('/recommend', {owner_id: id, owner_type: pathname.split('/')[1]}).value)
                setRecommend(true)
                setRecommendColor("#ee004b")
                GetAnyUserInfo(setRecommends, '/get_recommendations')
            }
        }
    }

    useEffect(() => {
        GetPersonalPageInfo(setPersonalPage, id)
    }, [setPersonalPage, id])

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
                        <AvatarsContainer user={PersonalPage.user} />
                    </Col>
                    <Col span={12}>
                        <Row>
                            <Button type="primary" htmlType="button" onClick={MakeLike} style={{background: likeColor}}
                                    icon={<LikeOutlined />} title="Likes">
                                {likes}
                            </Button>
                            <Button type="primary" htmlType="button" onClick={MakeDislike} title="Dislikes"
                                    style={{background: dislikeColor}} icon={<DislikeOutlined />}>
                                {dislikes}
                            </Button>
                            <Button type="primary" htmlType="button" onClick={MakeRecommend} title="Recommendations"
                                    style={{background: recommendColor}} icon={<CheckCircleOutlined />}>
                                {recommends}
                            </Button>
                            <Button type="primary" htmlType="button" title="Followers" icon={<TeamOutlined />}>
                                {followers}
                            </Button>
                            <Button type="primary" title="Followings" icon={<UserOutlined />}>
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