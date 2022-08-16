import React, {useState, useEffect} from "react";
import {GetAnyInfo} from "../../api/GeneralApi";
import {Button, Card, Descriptions, Popover, Tabs, Typography} from "antd";
import StaticAvatars from "../StaticRoutes";
import {useLocation, useParams} from "react-router-dom";
import {useNavigate} from "react-router";
import {UserOutlined} from "@ant-design/icons";
import makeAction from "../../api/PageActions";

const {Title} = Typography;
const { Meta } = Card;
const { TabPane } = Tabs;

const CommunityContainer = () => {
    const [community, setCommunity] = useState(null);
    const [owners, setOwners] = useState(null);
    const [access, setAccess] = useState(null);
    const [inCommunity, setInCommunity] = useState(null);
    const [subscribers, setSubscribers] = useState(null);
    const [participants, setParticipants] = useState(null);
    const [participantsForRemove, setParticipantsForRemove] = useState(null);
    const [dislike, setDislike] = useState(null);
    const [goals, setGoals] = useState(null);
    const [paymentGoals, setPaymentGoals] = useState(null);
    const [wallets, setWallets] = useState(null);
    const [like, setLike] = useState(null);
    const [recommend, setRecommend] = useState(null);
    const [conditions, setConditions] = useState(null);
    const [allow, setAllow] = useState(null);
    const [change, setChange] = useState(null);
    const {id} = useParams();
    const {pathname} = useLocation();

    const url = `/community/${id}`

    const navigate = useNavigate();

    useEffect(() => {
        const  CommunityInfo = (Community) => {
            setGoals(Community.goals)
            setOwners(Community.owners)
            setParticipants(Community.participants)
            // if (Community.owner) {
            //     setSubscribers(Community.subscribers)
            //     if (Community.subscribers) {
            //         setAddMembersAllow(true)
            //     }
            // }
            setConditions(Community.conditions)
            setInCommunity(Community.in_community)
            setCommunity(Community.community)
        }
        GetAnyInfo(CommunityInfo, url)
    }, [url, change])

    const Join = () => {
        makeAction('/join_community', {'community_id': id}, (value) => {
            setChange(value)
        }
        )
    }

    const Leave = () => {
        makeAction('/leave_community', {'community_id': id}, (value) => {
            setChange(value)
        }
        )
    }



    return (
        community ?
        <>
            <Descriptions title={community.community_name}>
                <Descriptions.Item label="Description">{community.community_bio}</Descriptions.Item>
                <Descriptions.Item label="Creator">{owners.map((owner, index)=>{
                    if (index===owners.length-1 && owners.length!==1){
                        return (<a href={`/user/${owner.user_id}`}>{owner.name + ' ' + owner.surname}</a>)

                    } else {
                        return (<a href={`/user/${owner.user_id}`}>{owner.name + ' ' + owner.surname + ','}</a>)
                    }

                }
                )}
                </Descriptions.Item>
            </Descriptions>
            <Popover content={
                    participants.map((participant) => {
                        return(<a href={'/user/' + participant.user_id} key={participant.user_id}><p key={participant.user_id}>{participant.name + ' ' + participant.surname}</p></a>)
                    })
                    } title="Participants" trigger="click">
                    <Button type="primary" title="Participants" icon={<UserOutlined />} >
                        {participants.length}
                    </Button>
            </Popover>
            {inCommunity ?
                    <>
                        <Button type="primary" onClick={Leave}>Leave</Button>
                    </>
                    :
                    <Button type="primary" onClick={Join}>Join</Button>
                }

        </>
        :
        <></>
    )
};
export default CommunityContainer;