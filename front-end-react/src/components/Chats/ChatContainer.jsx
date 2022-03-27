import React, {useEffect, useState} from "react";
import {GetAnyUserInfo} from "../../api/GeneralApi";
import {Avatar, List, Typography, Form, Input, Button, Popover, Select, Space} from "antd";
import StaticAvatars from "../StaticRoutes";
import {useLocation, useParams} from "react-router-dom";
import {useNavigate} from "react-router";
import {SendMessage, AddChatMembers, RemoveChatMembers} from "../../api/SendForms";


const ChatContainer = () => {
    const {Title} = Typography;
    const { Option } = Select;
    const {id} = useParams();
    const [Messages, setMessages] = useState(null);
    const [Participants, setParticipants] = useState(null);
    const [Subscribers, setSubscribers] = useState(null);
    const [Me, setMe] = useState(null);
    const [Block, setBlock] = useState(null);
    const [Message, setMessage] = useState("");
    const [Sended, setSended] = useState(null);
    const [Info, setInfo] = useState(null);
    const [VisibleAdd, setVisibleAdd] = useState(false);
    const [VisibleRemove, setVisibleRemove] = useState(false);
    const [MembersAdd, setMembersAdd] = useState(null);
    const [MembersRemove, setMembersRemove] = useState(null);
    const [Update, setUpdate] = useState(false);
    const navigate = useNavigate();
    const avatarPath = {0: StaticAvatars.StaticAvatars, 1: StaticAvatars.StaticGroupAvatars,
        2: StaticAvatars.StaticCommunityAvatars, 3: StaticAvatars.StaticCourseAvatars}

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
                setParticipants(ChatInfo.participants)
                setSubscribers(ChatInfo.subscribers)
                setInfo(ChatInfo.chat_info)
            }
        }
        GetAnyUserInfo(fillChatInfo, pathname)
    }, [pathname, Sended, Update])


    const MessagePositions = (item) => {
        setUpdate(false)
        setSended(false)
        item = item.item
        if (item.user_id === Me) {
                var style = {textAlign: 'right'}
            } else {
                var style = {}
            }
            return (
                    <List.Item.Meta
                        description={<p>{item.message} {item.datetime}</p>}
                        style={style}
                    />
            )
    }

    const onPressSend = e => {
        if (e.key === "Enter" && Message !== "") {
            SendForm();
        }
    }

    const SendForm = () => {
        SendMessage({'message': Message, 'chat_id': id,
            'chat_type': Messages[0]['chat_type']}, (data) => {
            setSended(data);
        })
        setMessage('');
    }

    const BackToChats = () => {
        navigate('/chats')
    }

    const hideAdd = () => {
        setVisibleAdd(false)
    };

    const hideRemove = () => {
        setVisibleRemove(false)
    };

    const handleVisibleAdd = () => {
        setVisibleAdd(true);
    };

    const handleVisibleRemove = () => {
        setVisibleRemove(true);
    };

    // const AddMember = () => {
    //     if (Info.chat_type === 1) {
    //         const options = []
    //         for (let i in Subscribers) {
    //             options.push(<Option key={Subscribers[i].user_id}>{Subscribers[i].surname + ' ' + Subscribers[i].name}</Option>)
    //                 }
    //         return (
    //             <Popover
    //                 content={
    //                     <div>
    //                         <Button type="primary" onClick={() => hide()}>X</Button>
    //                         <Form>
    //                             <Form.Item>
    //                                 <Select
    //                                     mode="multiple"
    //                                     allowClear
    //                                     style={{ width: '100%' }}
    //                                     placeholder="Please select"
    //                                     onChange={MemberChange}
    //                                 >
    //                                     {options}
    //                                 </Select>
    //                             </Form.Item>
    //                             <Button type="primary" onClick={() => Add()}>Add</Button>
    //                         </Form>
    //                     </div>
    //                 }
    //                 title="Add members"
    //                 trigger="click"
    //                 visible={visible}
    //                 onVisibleChange={handleVisibleChange}
    //             >
    //                 <Button type="primary">+</Button>
    //             </Popover>
    //
    //         )
    //     } else {
    //         return (<></>)
    //     }
    // }

    const MemberChange = (value) => {
        setMembersAdd(value)
    }

    const Add = () => {
        AddChatMembers({'chat_id': Info.chat_id, 'members': MembersAdd}, (data) => {
            setUpdate(data)
            setVisibleAdd(false)
        })
    }

    const RemoveChange = (value) => {
        setMembersRemove(value)
    }

    const Remove = () => {
        RemoveChatMembers({'chat_id': Info.chat_id, 'members': MembersRemove}, (data) => {
            setUpdate(data)
            setVisibleRemove(false)
        })
    }


    return (
        Info?
        <div>
            <Button onClick={BackToChats}>{'<'}</Button>
            <a href={Info.link}>{<Avatar src={avatarPath[Info.chat_type] + Info.href}/>} {<Title level={5}>{Info.title}</Title>}</a>
            <List
                itemLayout="horizontal"
                dataSource={Messages}
                renderItem={item =>
                    <MessagePositions item={item}/>
                }
            />
            {
                Block?
                    <p>U was blocked:(</p>
            :
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
                    >
                        <Input name="message" onChange={e => setMessage(e.target.value)}
                               onKeyPress={e => onPressSend(e)}/>
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
            }
            {Subscribers?
                <Popover name="subscribes"
                    content={
                        <div>
                            <Button type="primary" onClick={() => hideAdd()}>X</Button>
                            <Form>
                                <Form.Item>
                                    <Select
                                        mode="multiple"
                                        allowClear
                                        style={{ width: '100%' }}
                                        placeholder="Please select"
                                        onChange={MemberChange}
                                    >
                                        {Subscribers.map((sub) => {
                                            return (<Option key={sub.user_id}>{sub.surname + ' ' + sub.name}</Option>)
                                        })}
                                    </Select>
                                </Form.Item>
                                <Button type="primary" onClick={() => Add()}>Add</Button>
                            </Form>
                        </div>
                    }
                    title="Add members"
                    trigger="click"
                    visible={VisibleAdd}
                    onVisibleChange={handleVisibleAdd}
                >
                    <Button type="primary">+</Button>
                </Popover>
                :
                <></>}
            <Space>1</Space>
            {Participants?
                <Popover name="participants"
                    content={
                        <div>
                            <Button type="primary" onClick={() => hideRemove()}>X</Button>
                            <Form>
                                <Form.Item>
                                    <Select
                                        mode="multiple"
                                        allowClear
                                        style={{ width: '100%' }}
                                        placeholder="Please select"
                                        onChange={RemoveChange}
                                    >
                                        {Participants.map((par) => {
                                            return (<Option key={par.user_id}>{par.surname + ' ' + par.name}</Option>)
                                        })}
                                    </Select>
                                </Form.Item>
                                <Button type="primary" onClick={() => Remove()}>Remove</Button>
                            </Form>
                        </div>
                    }
                    title="Remove members"
                    trigger="click"
                    visible={VisibleRemove}
                    onVisibleChange={handleVisibleRemove}
                >
                    <Button type="primary">-</Button>
                </Popover>
                :
                <></>}
        </div>
            : <></>
    )
}

export default ChatContainer;