import React, {useEffect, useState} from "react";
import {GetAnyUserInfo} from "../../api/GeneralApi";
import {Avatar, List, Typography, Form, Input, Button} from "antd";
import StaticAvatars from "../StaticRoutes";
import {useLocation, useParams} from "react-router-dom";
import {useNavigate} from "react-router";
import SendMessage from "../../api/SendForms";


const ChatContainer = () => {
    const {Title} = Typography;
    const {id} = useParams();
    const [Messages, setMessages] = useState(null);
    const [Participants, setParticipants] = useState(null);
    const [Subscribers, setSubscribers] = useState(null);
    const [Me, setMe] = useState(null);
    const [Block, setBlock] = useState(null);
    const [ChatAvatar, setChatAvatar] = useState(null);
    const [ChatTitle, setChatTitle] = useState(null);
    const [ToPage, setToPage] = useState(null);
    const [Message, setMessage] = useState("");
    const [Sended, setSended] = useState(null);
    const navigate = useNavigate();


    const {pathname} = useLocation();

    useEffect(() => {
        const fillChatInfo = (ChatInfo) => {
            if (ChatInfo.forbidden) {
                return null
            } else {
                setMessages(ChatInfo.messages)
                setParticipants(ChatInfo.participants)
                setSubscribers(ChatInfo.subscribers)
                setMe(ChatInfo.me)
                setBlock(ChatInfo.block)
            }
        }
        GetAnyUserInfo(fillChatInfo, pathname)
    }, [pathname, Sended])


    const MessagePositions = (item) => {
        item = item.item
        if (item.chat_type === 0) {
            if (item.user_id === Me) {
                var style = {textAlign: 'right'}
            } else {
                var style = {}
                setChatAvatar(StaticAvatars.StaticAvatars + item.href)
                setChatTitle(item.surname + ' ' + item.name)
                setToPage(`/user/${item.user_id}`)
            }
            return (
                    <List.Item.Meta
                        description={<p>{item.message} {item.datetime}</p>}
                        style={style}
                    />
            )
        } else if (item.chat_type === 1) {
            if (item.user_id === Me) {
                var style = {textAlign: 'right'}
            } else {
                var style = {}
                setChatAvatar(StaticAvatars.StaticGroupAvatars + item.group_avatar)
                setChatTitle(item.group_name)
                setToPage(`/user/${item.user_id}`)
            }
            return (
                    <List.Item.Meta
                        description={<p>{item.message} {item.datetime}</p>}
                        style={style}
                    />
            )
        } else {
            return (<></>)
        }
    }

    const ISForm = () => {
        if (Block) {
            return (<p>U was blocked:(</p>)
        } else {
            return (
                <div>
                    <Form
                        labelCol={{
                            span: 6,
                        }}
                        wrapperCol={{
                            span: 8,
                        }}
                        initialValues={{
                            remember: false,
                        }}
                        autoComplete="off"
                    >
                        <Form.Item
                            name="message"
                            onChange={e => setMessage(e.target.value)}
                            onKeyPress={e => onPressSend(e)}
                        >
                            <Input value={Message} />
                        </Form.Item>
                        <Form.Item
                            wrapperCol={{
                                offset: 8,
                                span: 8
                            }}
                        >
                            <Button type="primary" htmlType="button" onClick={() => SendForm()}>
                                    Send
                            </Button>
                        </Form.Item>
                    </Form>
                </div>
            )
        }
    }

    const onPressSend = e => {
        if (e.key === "Enter" && Message !== "") {
            SendForm();
        }
    }

    const SendForm = () => {
        if (Message !== "") {
            {SendMessage('/send_message', {'message': Message, 'chat_id': id,
                'chat_type': Messages[0]['chat_type']}, (data) => {
                setSended(data);
                // to do: clear input
                setMessage("");
                console.log(Message)
            })
            }
        } else {
            return null
        }
    }

    const BackToChats = () => {
        navigate('/chats')
    }

    return (
        Messages?
        <div>
            <Button onClick={BackToChats}>{'<'}</Button>
            <a href={ToPage}>{<Avatar src={ChatAvatar}/>} {<Title level={5}>{ChatTitle}</Title>}</a>
            <List
                itemLayout="horizontal"
                dataSource={Messages}
                renderItem={item =>
                    <MessagePositions item={item}/>
                }
            />
            {ISForm()}
        </div>
            : <></>
    )
}

export default ChatContainer;