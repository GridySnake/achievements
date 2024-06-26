import React, {useEffect, useState} from "react";
import {GetAnyInfo, GetSubspheresBySphere, GetConditionsByGroup, GetConditionsByService,
    GetConditionsByAggregation, GetUsersByType} from "../../api/GeneralApi";
import {Avatar, Button, Form, Input, List, Select, Skeleton, Tabs, DatePicker} from "antd";
import StaticQR from "../StaticRoutes";
import makeAction from "../../api/PageActions";
import {useNavigate, useParams} from "react-router";
import {Option} from "antd/es/mentions";
// import { YMaps, Map, Placemark } from "react-yandex-maps";
import { Image } from 'antd';
import {useLocation} from "react-router-dom";
import { Descriptions } from 'antd';
import AchievementGeoContainer from "./AchievementGeoContainer";

const AchievementContainer = () => {
    const [group, setGroup] = useState(null);
    const [aggregate, setAggregate] = useState(null);
    const [created, setCreated] = useState(null);
    const [description, setDescription] = useState(null);
    const [is_new, setNew] = useState(null);
    const [sphere, setSphere] = useState(null);
    const [status, setStatus] = useState(0);
    const [subsphere, setSubsphere] = useState(null);
    const [geo, setGeo] = useState(null);
    const [test, setTest] = useState(null);
    const [title, setTitle] = useState(null);
    const [values, setValues] = useState(null);
    const [owner, setOwner] = useState(null);
    const [desire, setDesire] = useState(null);
    const [isOwner, setIsOwner] = useState(null);
    const [qr, setQr] = useState(null);
    const [visible, setVisible] = useState(false);
    const [coords, setCoords] = useState(false);
    const [isReached, setIsReached] = useState(false);
    const {pathname} = useLocation();
    const navigate = useNavigate();
    const {id} = useParams();

    useEffect(() => {
        const setInfoAchievement = (Achievement_info) => {
            const Achievement = Achievement_info.achievement
            setTitle(Achievement.name)
            setDescription(Achievement.description)
            setCreated(Achievement.created_date)
            setGroup(Achievement.achi_condition_group_name)
            setAggregate(Achievement.aggregate_name)
            setNew(Achievement.new)
            setSphere(Achievement.sphere_name)
            setSubsphere(Achievement.subsphere_name)
            setGeo(Achievement.geo)
            setTest(Achievement.test_url)
            setIsReached(Achievement_info.is_reached)
            if (Achievement.achi_condition_group_id === 1) {
                setQr(StaticQR.StaticQR + Achievement.value + '.front_png')
            } else {
                setValues(Achievement.value)
            }
            setDesire(Achievement_info.desire)
            setIsOwner(Achievement_info.is_owner)
            setOwner(<a href={'/user/' + Achievement.user_id}>{Achievement.u_name + ' ' + Achievement.u_surname}</a>)
        }
        GetAnyInfo(setInfoAchievement, pathname)
    }, [pathname, desire])

    const DesireText = () => {
        if (desire) {
            return 'Undesire'
        } else {
            return 'Desire'
        }
    }

    const Delete = () => {
        makeAction('/drop_achievement', {'achievement_id': id, 'user_type': 0}, (value) => {
        })
    }

    const VerifyDesire = () => {
        if (desire) {
            makeAction('/undesire', {'achievement_id': id, 'user_type': 0}, (value) => {
                setDesire(value.desire)
        })
        } else {
            if (group === 'Geolocation') {
                makeAction('/verify_achievement_geo', {'achievement_id': id, 'user_type': 0,
                    'lat': geopos.props.children[1], 'lon': geopos.props.children[2],
                    'accuracy': geopos.props.children[3]}, (value) => {
                    setIsReached(value.is_reached)
                    setDesire(value.desire)
                })
            } else {
                makeAction('/verify_achievement', {'achievement_id': id, 'user_type': 0}, (value) => {
                setDesire(value.desire)
                setIsReached(value.is_reached)
            })
            }
        }
    }

    const Verify = () => {
        if (group === 'Geolocation') {
                makeAction('/verify_achievement_geo', {'achievement_id': id, 'user_type': 0,
                    'lat': geopos.props.children[1], 'lon': geopos.props.children[2],
                    'accuracy': geopos.props.children[3]}, (value) => {
                    setIsReached(value.is_reached)
                    setDesire(value.desire)
                })
            } else {
            makeAction('/verify_achievement', {'achievement_id': id, 'user_type': 0}, (value) => {
                setIsReached(value.is_reached)
                setDesire(value.desire)
            })
        }
    }

    const geopos = AchievementGeoContainer()
    console.log(geopos.props.children[1])

    return (
        owner?
            <>
                <Descriptions title={title}>
                    <Descriptions.Item label="Description">{description}</Descriptions.Item>
                    <Descriptions.Item label="Sphere">{sphere}</Descriptions.Item>
                    <Descriptions.Item label="Creator">{owner}</Descriptions.Item>
                    <Descriptions.Item label="Group">{group}</Descriptions.Item>
                    <Descriptions.Item label="Subsphere">{subsphere}</Descriptions.Item>
                    <Descriptions.Item label="Created">{created}</Descriptions.Item>
                    {values?
                        <Descriptions.Item label="Value">{values}</Descriptions.Item>
                        :
                        <></>
                    }
                    <Descriptions.Item label=""></Descriptions.Item>
                    <Descriptions.Item label=""></Descriptions.Item>

                </Descriptions>
                {test?
                    <Button onClick={()=> window.open(test, "_blank")}>Test</Button>
                    :
                    <></>
                }
                {qr && isOwner?
                    <>
                        <Image
                            preview={{ visible: false }}
                            width={200}
                            src={qr}
                            onClick={() => setVisible(true)}
                        />
                        <div style={{ display: 'none' }}>
                            <Image.PreviewGroup preview={{ visible, onVisibleChange: vis => setVisible(vis) }}>
                                <Image src={qr}/>
                            </Image.PreviewGroup>
                        </div>
                    </>
                    :
                    <></>
                }
                {geo ?
                    <></>
                    // <YMaps>
                    //     <div>
                    //         <Map defaultState={{center: geo[0], zoom: 12}}>
                    //             <Placemark
                    //                 geometry={geo[0]}
                    //             />
                    //         </Map>
                    //     </div>
                    // </YMaps>

                    :
                    <></>
                }
                {!isOwner && !isReached ?
                    <Button onClick={VerifyDesire}>{DesireText()}</Button>
                    :
                    <></>
                }
                {!isOwner && !isReached && desire && group !== 'User approvement' ?
                    <Button onClick={Verify}>Verify</Button>
                    :
                    <></>
                }
                {isOwner?
                    <>
                        <Button>Delete</Button>
                        <Button>Edit</Button>
                    </>
                    :
                    <></>
                }
            </>
            :
            <></>
    )
}

export default AchievementContainer;