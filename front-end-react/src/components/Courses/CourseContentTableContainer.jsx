import React, { useState, useEffect } from "react";
import { GetAnyInfo } from "../../api/GeneralApi";
import { useParams } from "react-router-dom";
import { Collapse } from 'antd'
const { Panel } = Collapse;


const CourseContentTableContainer = () => {
    const [contents, setContents] = useState(null);

    const {id} = useParams();

    const url = `/study_course/${id}`

    useEffect(() => {
        const ContentsInfo = (Content) => {
            setContents(Content.navigation)
        }
        GetAnyInfo(ContentsInfo, url)
    }, [url])

    const onChange = (key: string | string[]) => {
        console.log(key);
    };

    const check = () => {
        console.log(contents)
        console.log([...new Map(contents
                                        .filter(item => item.title === "Chapter1")
                                        .map((item) => [item["subtitle"], item]).values())])
    }

    return(
        contents?
            <div>
                {check()}
                <Collapse onChange={onChange}>
                    {
                        [...new Map(contents.map((item) => [item["title"], item])).values()]
                        .map((content_title, index) => (
                            content_title.title?
                            <Panel key={index} header={content_title.title}>
                                <Collapse onChange={onChange}>
                                    {
                                        [...new Map(contents
                                            .filter(item => item.title === content_title.title)
                                            .map((item) => [item["subtitle"], item]).values())]
                                            .map((content_sub, index) => (
                                                content_sub[0]?
                                        <Panel key={index} header={content_sub[0]}>
                                            {
                                                contents
                                                    .filter(item => item.title === content_title.title &&
                                                        item.subtitle === content_sub[0])
                                                    .map((content) => (
                                                <a href={url+ '/task/' + content.content_page}><p>{content.content_name}</p></a>
                                            ))
                                            }
                                        </Panel>
                                                    :
                                                    <p>
                                                    {
                                                contents
                                                    .filter(item => item.title === content_title.title &&
                                                        item.subtitle === null)
                                                    .map((content) => (
                                                <a href={url+ '/task/' + content.content_page}><p>{content.content_name}</p></a>
                                            ))
                                            }
                                            </p>
                                ))
                                }
                                </Collapse>
                            </Panel>
                                :
                                <Collapse onChange={onChange}>
                                    {
                                        [...new Map(contents
                                            .filter(item => item.title === null)
                                            .map((item) => [item["subtitle"], item]).values())]
                                            .map((content_sub, index) => (
                                                content_sub[0]?
                                        <Panel key={index} header={content_sub[0]}>
                                            {
                                                contents
                                                    .filter(item => item.title === content_title.title &&
                                                        item.subtitle === content_sub[0])
                                                    .map((content) => (
                                                <a href={url+ '/task/' + content.content_page}><p>{content.content_name}</p></a>
                                            ))
                                            }
                                        </Panel>
                                                    :
                                                    <p>
                                                    {
                                                contents
                                                    .filter(item => item.title === null &&
                                                        item.subtitle === null)
                                                    .map((content) => (
                                                <a href={url+ '/task/' + content.content_page}><p>{content.content_name}</p></a>
                                            ))
                                            }
                                            </p>
                                ))
                                }
                            </Collapse>
                        ))
                    }
                </Collapse>
            </div>
            :
            <></>
    )
};

export default CourseContentTableContainer;