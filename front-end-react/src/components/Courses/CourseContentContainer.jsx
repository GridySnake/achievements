import React, {useState, useEffect} from "react";
import {Avatar, Button, Card, Col, Descriptions, Image, List, Skeleton, Tabs, Typography, Popover, Select, Form} from "antd";
import {GetAnyInfo} from "../../api/GeneralApi";
import StaticAvatars from "../StaticRoutes";
import {useLocation, useParams} from "react-router-dom";
import {UserOutlined} from "@ant-design/icons";
import makeAction from "../../api/PageActions";
import { Collapse } from 'antd'
// import {useNavigate} from "react-router";
const { Option } = Select;
const {Title} = Typography;
const { Meta } = Card;
const { TabPane } = Tabs;
const { Panel } = Collapse;
// const navigate = useNavigate();


const CourseContentContainer = () => {
    const [contents, setContents] = useState(null);

    const {id} = useParams();

    const url = `/study_course/${id}`

    useEffect(() => {
        const  ContentInfo = (Content) => {
            setContents(Content.navigation)
        }
        GetAnyInfo(ContentInfo, url)
    }, [url])
    const text = 'text'

    const onChange = (key: string | string[]) => {
        console.log(key);
    };

    return(
        contents?
            <div>
                <Collapse onChange={onChange}>
                    {contents.map((content) => {
                        if (content.is_title) {
                            return (<Panel header={content.content_name} key={content_page}><Collapse/>)
                                }
                        } else if (content.is_subtitle) {
                                return (<Panel header={content.content_name} key={content_page}>)
                                }
                    })
                    <Panel header="This is panel header 1" key="1">
                        <Collapse defaultActiveKey="1">
                            <Panel header="This is panel nest panel" key="1">
                                <p>{text}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="This is panel header 2" key="2">
                        <p>{text}</p>
                    </Panel>
                    <Panel header="This is panel header 3" key="3">
                        <p>{text}</p>
                    </Panel>
                </Collapse>
                {/*<Timeline>*/}
                {/*    {contents.map((content) => {*/}
                {/*        return (<Timeline.Item key={content.page}>{content.content_name }</Timeline.Item>)*/}
                {/*    })}*/}
                {/*  </Timeline>*/}
            </div>
            :
            <></>
    )
};

export default CourseContentContainer;