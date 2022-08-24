import React, {useState, useEffect } from "react";
import { Image, Card, Typography, Row, Col, Button } from "antd";
import { LikeOutlined, DislikeOutlined, CheckCircleOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons';
import GetPersonalPageInfo from "../../api/Api";
import StaticAvatars from "../StaticRoutes";
import AvatarsContainer from "./AvatarsContainer";
import { useParams, useLocation } from 'react-router-dom'
import makeAction from "../../api/PageActions";
import GoalsApproveContainer from "./GoalsApproveContainer";
import styles from '../css/PersonalPageContainer.module.css'
import styleStatistincs from '../css/StatisticsContainer.module.css'
import StaticFrontPng from "../StaticRoutes";
import InterestsBubblesContainer from "./InterestsBubblesContainer";


const StaticFront = StaticFrontPng.StaticFrontPng

const PersonalPageContainer = () => {
    const [PersonalPage, setPersonalPage] = useState(null);
    const [likeImage, setLikeImage] = useState(null);
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
    const [courses, setCourses] = useState(null);
    const [interestsSphere, setInterestsSphere] = useState(null);
    const [interestsSubsphere, setInterestsSubsphere] = useState(null);
    const [needBubble, setNeedBubble] = useState(null);
    const [hoverTag, setHoverTag] = useState(null);
    const [myPage, setMyPage] = useState(null);
    const [approve, setApprove] = useState(null);
    const [isApproved, setIsApproved] = useState(null);
    const [approveGot, setApproveGot] = useState(null);
    const [isApprovedGot, setIsApprovedGot] = useState(null);
    const [owner, setOwner] = useState(null);
    const [reload, setReload] = useState(0);

    const {id} = useParams();
    const {pathname} = useLocation();


    useEffect(() => {
        const fillUserInfo = (PersonalPage) => {
            if (PersonalPage.need_verify) {
                PersonalPage.need_verify.map((achievement) => {
                    makeAction('/verify_achievement', {'achievement_id': achievement,
                        'user_id': id, 'user_type': 0}, (value) => {
                        setReload(reload+1)
                    })
                })
            }
            setLike(PersonalPage.actions[0])
            setDislike(PersonalPage.actions[1])
            setRecommend(PersonalPage.actions[2])
            setLikeImage(imageLike(PersonalPage.actions[0]))
            setDislikeColor(color(PersonalPage.actions[1]))
            setRecommendColor(color(PersonalPage.actions[2]))
            setLikes(PersonalPage.statistics.likes)
            setDislikes(PersonalPage.statistics.dislikes)
            setRecommends(PersonalPage.statistics.recommendations)
            setFollowers(PersonalPage.statistics.followers)
            setFollowings(PersonalPage.statistics.followings)
            setCourses(PersonalPage.statistics.join_courses)
            setMyPage(pointEvent(PersonalPage.myPage))
            setApprove(PersonalPage.approve)
            setIsApproved(PersonalPage.is_approved)
            setOwner(PersonalPage.myPage)
            setApproveGot(PersonalPage.approve_got)
            setIsApprovedGot(PersonalPage.is_approved_got)
            setInterestsSphere({'interest': PersonalPage.interests_sphere})
            setInterestsSubsphere(PersonalPage.interests_subsphere)
            setPersonalPage(PersonalPage)

        }
        GetPersonalPageInfo(fillUserInfo, id)
    }, [id, reload])

    const CardReturn = (post) => {
        if (post.href) {
            return <Image src={StaticAvatars.StaticPosts + post.href}/>;
        } else {
            return <></>;
        }}

    const imageLike = (bool) => {
        if (bool) {
            return 'like_inactive.png'
        } else {
            return 'like_active.png'
        }
    }

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
                setLikeImage('like_inactive.pnd')
                setLikes(value)
            })

        } else {
            makeAction('/like', {owner_id: id, owner_type: pathname.split('/')[1]}, (value) => {
                setLike(true)
                setLikeImage('like_active.png')
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
    const props = {
        'approve': approve,
        'is_approved': isApproved,
        'approve_got': approveGot,
        'is_approved_got': isApprovedGot,
        'owner': owner,
        'id': id
    }

    const Detailed = (index) => {
        setNeedBubble(index)
        setHoverTag(interestsSphere[index].sphere_name)
    }

    const UnDetailed = () => {
        setNeedBubble(null)
        setHoverTag(null)
    }

    const Hover = (value) => {
        setHoverTag(value)
    }

    const UnHover = () => {
        setHoverTag(null)
    }

    return (
        PersonalPage ?
            <div>
                <div className={styles.groupDivInfo}>
                    <div className={styles.Div2} />
                    <div className={styles.Div3} />
                    <AvatarsContainer user={PersonalPage.user} />
                    <b className={styles.nameAge}>{PersonalPage.user.name + ' ' + PersonalPage.user.surname + ', ' + PersonalPage.user.age}</b>
                    <div className={styles.cityCountry}>{PersonalPage.user.city + ', ' + PersonalPage.user.country}</div>
                    <div className={styles.bio}>{PersonalPage.user.bio}</div>
                    <img className={styles.employeeIcon} alt="" src={StaticFront + 'employee.png'} />
                    <div className={styles.employeeName}>1C Game Studios</div>
                    <div className={styles.employeeTag}>Employee</div>
                </div>

                <div className={styles.interestsDiv}>
                    <div className={styles.interestsDiv1} />
                    <div className={styles.bubbleHoverTag}>{hoverTag}</div>
                    <div className={styles.bubbleDiv}>
                        {<InterestsBubblesContainer {...interestsSphere}/>}
                        {/*{interestsSphere?*/}
                        {/*    interestsSphere.map((interest, index) => {*/}
                        {/*        if (needBubble !== null) {*/}
                        {/*            if (index !== needBubble) {*/}
                        {/*                return (<div key={index} className={styles.circleNoActive}*/}
                        {/*                             onClick={() => Detailed(index)}*/}
                        {/*                >{interest.count_achievements}</div>)*/}
                        {/*            } else {*/}
                        {/*                return (<div key={index} className={styles.circleActive}*/}
                        {/*                             onClick={() => UnDetailed()}*/}
                        {/*                >{interest.count_achievements}</div>)*/}
                        {/*            }*/}
                        {/*        } else {*/}
                        {/*            return (<div key={index} className={styles.circleDefault} onMouseEnter={() => Hover(interest.sphere_name)}*/}
                        {/*                             onMouseLeave={UnHover} onClick={() => Detailed(index)}*/}
                        {/*                >{interest.count_achievements}</div>)*/}
                        {/*        }*/}
                        {/*    })*/}
                        {/*    :*/}
                        {/*    <></>*/}
                        {/*}*/}
                    </div>
                    <div className={styles.interestsTag}>Interests</div>
                </div>
                <>
                    <div className={styleStatistincs.groupDiv}>
                        <div className={styleStatistincs.e529a00d39108817f5cb7aea883a4Div} />
                        <img
                            className={styleStatistincs.recommendationsIcon}
                            alt=""
                            src={StaticFront + 'recommendations.png'}
                            onClick={!myPage? MakeRecommend : false}
                        />
                        <img
                            className={styleStatistincs.tablerchevronsDownIcon}
                            alt=""
                            src={StaticFront + 'arrow_hide.png'}
                        />
                        <img
                            className={styleStatistincs.dislikeIcon}
                            alt=""
                            src={StaticFront + 'dislike.png'}
                            onClick={!myPage? MakeDislike : false}
                        />
                        <img
                            className={styleStatistincs.likeIcon}
                            alt=""
                            src={StaticFront + likeImage}
                            onClick={!myPage? MakeLike : false}
                        />
                        <img
                            className={styleStatistincs.subscribersIcon}
                            alt=""
                            src={StaticFront + 'subscribers.png'}
                        />
                        <img
                            className={styleStatistincs.coursesIcon}
                            alt=""
                            src={StaticFront + 'courses.png'}
                        />
                        <div className={styleStatistincs.likeText}>{likes}</div>
                        <div className={styleStatistincs.subscribersText}>{followers}</div>
                        <div className={styleStatistincs.recommendationsText}>{recommends}</div>
                        <div className={styleStatistincs.coursesText}>{courses}</div>
                        <div className={styleStatistincs.dislikeText}>{dislikes}</div>
                        <div className={styleStatistincs.infoDiv}>Info</div>
                    </div>
                </>

                {/*<Button type="primary" htmlType="button" onClick={MakeLike} style={{background: likeColor,*/}
                {/*                pointerEvents: pEvent}}*/}
                {/*                    icon={<LikeOutlined />} title="Likes">*/}
                {/*                {likes}*/}
                {/*</Button>*/}
                {/*<Button type="primary" htmlType="button" onClick={MakeDislike} title="Dislikes"*/}
                {/*                    style={{background: dislikeColor, pointerEvents: pEvent}} icon={<DislikeOutlined />}>*/}
                {/*                {dislikes}*/}
                {/*</Button>*/}
                {/*<Button type="primary" htmlType="button" onClick={MakeRecommend} title="Recommendations"*/}
                {/*                    style={{background: recommendColor, pointerEvents: pEvent}} icon={<CheckCircleOutlined />}>*/}
                {/*                {recommends}*/}
                {/*</Button>*/}
                {/*<Button type="primary" title="Followers" style={{pointerEvents: "none"}} icon={<TeamOutlined />}>*/}
                {/*                {followers}*/}
                {/*</Button>*/}
                {/*<Button type="primary" title="Followings" style={{pointerEvents: "none"}} icon={<UserOutlined />}>*/}
                {/*                {followings}*/}
                {/*</Button>*/}
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

                {approve || approveGot ?
                    <GoalsApproveContainer {...props}/>
                    :
                    <></>
                }
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