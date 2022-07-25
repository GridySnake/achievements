import React, {useEffect, useState} from "react";
import {GetAnyInfo} from "../../api/GeneralApi";
import {Avatar, List, Card, Tabs, Button, Drawer, Form, Col, Row, Input, Space, Upload} from "antd";
import { PlusOutlined, InboxOutlined } from '@ant-design/icons';
import StaticAvatars from "../StaticRoutes";
import {useNavigate} from "react-router";
import {CreateGroupChat} from "../../api/SendForms";
import {UploadStatic} from "../../api/AvatarAction";

const { TabPane } = Tabs;

const ChatsContainer = () => {
    const [Users, setUsers] = useState(null);
    const [Groups, setGroups] = useState(null);
    const [Communities, setCommunities] = useState(null);
    const [Courses, setCourses] = useState(null);
    const navigate = useNavigate();
    const url = '/messages'
    const [visible, setVisible] = useState(false);
    const [GroupName, setGroupName] = useState(null);
    const [File, setFile] = useState(null);
    const [progress, setProgress] = useState(0);
    const [Image, setImage] = useState(null);

    useEffect(() => {
        const setInfoChats = (Chats) => {
            setUsers(Chats.users)
            setGroups(Chats.groups)
            setCommunities(Chats.communities)
            setCourses(Chats.courses)
        }
        GetAnyInfo(setInfoChats, url)
    }, [url])

    const toChat = (id) => {
        navigate(`/chat/${id}`)
    }

    const Message = (message) => {
        message = message.message
        if (message.name === message.m_name && message.surname === message.m_surname) {
                var me = ''
            } else {
                var me = 'You: '
            }
        return (
                message.message?
                <div>
                    <p>{me + ' ' + message.message + ' ' + message.datetime}</p>
                </div>
                    : <></>
            )
        // } else if (message.chat_type === 1) {
        //     return (
        //         message.message?
        //         <div>
        //             <p>{message.m_name + ' ' + message.m_surname}</p>
        //             <p>{message.message + ' ' + message.datetime}</p>
        //         </div>
        //             : <></>
        //     )
        // }
        // else {
        //     return (
        //         <></>
        //     )
        // }

        // return (
        //     message.message?
        //     <div>
        //         message.message
        //         message.datetime
        //         message.
        //         message.
        //     </div>
        //         : <></>
        // )
    }

    const showDrawer = () => {
        setVisible(true);
    };

    const onClose = () => {
        setVisible(false);
    };

    const onPressSend = e => {
        if (e.key === "Enter" && GroupName !== "") {
            GroupChat();
        }
    }

    const GroupChat = () => {
        CreateGroupChat({'chat_name': GroupName, 'image_id': Image}, (data) => {
        navigate(`/chat/${data}`)
        })
    }

    // const normFile = (e: any) => {
    //   console.log('Upload event:', e);
    //   if (Array.isArray(e)) {
    //     return e;
    //   }
    //   return e && e.fileList;
    // };

    // const onFileUpload = () => {
    //     const formData = new FormData();
    //     formData.append(
    //         "group_avatar",
    //         File,
    //         File.name
    //     );
    //     return formData
    // }

    // const props = {
    //     customRequest: ({file}) => UploadStatic(file),
    // beforeUpload: file => {
    //   const isPNG = file.type === 'image/png';
    //   if (!isPNG) {
    //     console.log(`${file.name} is not a png file`);
    //   }
    //   return isPNG || Upload.LIST_IGNORE;
    // },
    // onChange: info => {
    //   console.log(info.fileList);
    // },
    // };

    const uploadImage = async options => {
    const { file, onProgress } = options;

    const fmData = new FormData();
    const config = {
      headers: { "content-type": "multipart/form-data" },
      onUploadProgress: event => {
        const percent = Math.floor((event.loaded / event.total) * 100);
        setProgress(percent);
        if (percent === 100) {
          setTimeout(() => setProgress(0), 1000);
        }
        onProgress({ percent: (event.loaded / event.total) * 100 });
      }
    };
    fmData.append("image", file);
    UploadStatic(fmData, config, '/upload_group_avatar', (data) => {
        setImage(data)
    })
  };

    return (
        Users?
        <Tabs defaultActiveKey="Direct">
            <TabPane tab="Direct chats" key="Direct">
                <List
                    itemLayout="horizontal"
                    dataSource={Users}
                    renderItem={item => {
                        if (item.message !== null) {
                            return(
                            <Card onClick={() => toChat(item.chat_id)}>
                                <List.Item.Meta
                                    avatar={<Avatar src={StaticAvatars.StaticAvatars + item.href}/>}
                                    title={<a href={'/user/' + item.user_id}>{item.name + ' ' + item.surname}</a>}
                                />
                                <Message message={item}/>
                            </Card>
                            )
                        } else {
                            return (<></>)
                        }
                    }}
                />
            </TabPane>
            <TabPane tab="Group chats" key="Groups">
                <List
                    itemLayout="horizontal"
                    dataSource={Groups}
                    renderItem={item => {
                        if (item.message !== null) {
                            return(
                                <Card onClick={() => toChat(item.chat_id)}>
                                    <List.Item.Meta
                                        avatar={<Avatar src={StaticAvatars.StaticGroupAvatars + item.href}/>}
                                        title={<a href={'/chat/' + item.chat_id}>{item.group_name}</a>}
                                    />
                                    <Message message={item}/>
                                </Card>
                                )
                        } else {
                            return (<></>)
                        }
                    }}
                />
                <Button type="primary" onClick={() => showDrawer()} icon={<PlusOutlined />}>
                    New chat
                </Button>
                <Drawer
                    title="Create a new chat"
                    width={720}
                    onClose={() => onClose()}
                    visible={visible}
                    bodyStyle={{ paddingBottom: 80 }}
                    extra={
                        <Space>
                            <Button onClick={() => onClose()}>Cancel</Button>
                            <Button onClick={() => GroupChat()} type="primary">Submit</Button>
                        </Space>
                        }
                >
                    <Form layout="vertical" hideRequiredMark>
                        <Row gutter={16}>
                            <Col span={12}>
                                <Form.Item
                                    name="chat name"
                                    label="Chat name"
                                    rules={[{ required: true, message: 'Please enter chat name' }]}
                                    onChange={e => setGroupName(e.target.value)}
                                    onKeyPress={e => onPressSend(e)}
                                >
                                    <Input placeholder="Chat name" />
                                </Form.Item>
                            </Col>
                            <Col span={12}>
                                <Form.Item name="dragger" valuePropName="fileList" getValueFromEvent={e => setFile(e.target)} noStyle>
                                    <Upload.Dragger name="files" customRequest={uploadImage} multiple={false}>
                                    <p className="ant-upload-drag-icon">
                                      <InboxOutlined />
                                    </p>
                                  </Upload.Dragger>
                                </Form.Item>
                            </Col>
                        </Row>
                    </Form>
                </Drawer>
            </TabPane>
            <TabPane tab="Community chats" key="Communities">
                <List
                    itemLayout="horizontal"
                    dataSource={Communities}
                    renderItem={item => {
                        if (item.message !== null) {
                            return(
                                <Card onClick={() => toChat(item.chat_id)}>
                                    <List.Item.Meta
                                        avatar={<Avatar src={StaticAvatars.StaticCommunityAvatars + item.href}/>}
                                        title={<a href={'/community/' + item.community_id}>{item.community_name}</a>}
                                    />
                                    <Message message={item}/>
                                </Card>
                                )
                        } else {
                            return (<></>)
                        }
                    }}
                />
            </TabPane>
            <TabPane tab="Course chats" key="Courses">
                <List
                    itemLayout="horizontal"
                    dataSource={Courses}
                    renderItem={item => {
                        if (item.message !== null) {
                            return(
                                <Card onClick={() => toChat(item.chat_id)}>
                                    <List.Item.Meta
                                        avatar={<Avatar src={StaticAvatars.StaticCourseAvatars + item.href}/>}
                                        title={<a href={'/course/' + item.course_id}>{item.course_name}</a>}
                                    />
                                    <Message message={item}/>
                                </Card>
                                )
                        } else {
                            return (<></>)
                        }
                    }}
                />
            </TabPane>
        </Tabs>
            : <></>
    )
}


export default ChatsContainer;