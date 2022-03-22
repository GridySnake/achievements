import React, {useEffect, useState} from "react";
import {GetAnyUserInfo} from "../../api/GeneralApi";
import {Avatar, List, Card} from "antd";
import StaticAvatars from "../StaticRoutes";
import {useParams} from "react-router-dom";

const ChatsContainer = () => {

    const [Chat, setChat] = useState(null);
    const {id} = useParams();

    useEffect(() => {
        const fillChatInfo = (ChatInfo) => {
            setChat(ChatInfo)
        }
        GetAnyUserInfo(fillChatInfo, id)
    }, [id])

    return (
        Chat?
        <div>1</div>
            : <></>
    )
}

export default ChatsContainer;