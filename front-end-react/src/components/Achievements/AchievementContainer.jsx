import React, {useEffect, useState} from "react";
import {GetAnyInfo, GetSubspheresBySphere, GetConditionsByGroup, GetConditionsByService,
    GetConditionsByAggregation, GetUsersByType} from "../../api/GeneralApi";
import {Avatar, Button, Form, Input, List, Select, Skeleton, Tabs, DatePicker} from "antd";
import StaticQR from "../StaticRoutes";
import makeAction from "../../api/PageActions";
import {useNavigate} from "react-router";
import {Option} from "antd/es/mentions";
import {useLocation} from "react-router-dom";
import { Descriptions } from 'antd';

const AchievementContainer = () => {
    const [group, setGroup] = useState(null);
    const [aggregate, setAggregate] = useState(null);
    const [created, setCreated] = useState(null);
    const [description, setDescription] = useState(null);
    const [is_new, setNew] = useState(null);
    const [sphere, setSphere] = useState(null);
    const [subsphere, setSubsphere] = useState(null);
    const [geo, setGeo] = useState(null);
    const [test, setTest] = useState(null);
    const [title, setTitle] = useState(null);
    const [values, setValues] = useState(null);
    const [owner, setOwner] = useState(null);
    const [desire, setDesire] = useState(null);
    const [isOwner, setIsOwner] = useState(null);
    const {pathname} = useLocation();

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
            setOwner(Achievement.u_name + ' ' + Achievement.u_surname)
            setValues(Achievement.value)
            setDesire(Achievement_info.desire)
            setIsOwner(Achievement_info.is_owner)
        }
        GetAnyInfo(setInfoAchievement, pathname)
    }, [pathname])

    const DesireText = () => {
        if (desire) {
            return 'Undesire'
        } else {
            return 'Desire'
        }
    }

    return (
        owner?
            <>
            <Descriptions title={title}>
                <Descriptions.Item label="Description">{description}</Descriptions.Item>
                <Descriptions.Item label="Sphere">{sphere}</Descriptions.Item>
                <Descriptions.Item label="Creator">{owner}</Descriptions.Item>
                <Descriptions.Item label="Value">{values}</Descriptions.Item>
                <Descriptions.Item label="Subsphere">{subsphere}</Descriptions.Item>
                <Descriptions.Item label="Created">{created}</Descriptions.Item>
            </Descriptions>
            {test?
                <Button onClick={()=> window.open(test, "_blank")}>Test</Button>
                :
                <></>
            }
            <Button>{DesireText()}</Button>
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
            <>1</>
    )
}

export default AchievementContainer;