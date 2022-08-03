import React, { useState, useEffect } from "react";
import { Typography, Button } from "antd";
import { GetAnyInfo } from "../../api/GeneralApi";
import { useParams } from "react-router-dom";
import ReactPlayer from 'react-player'
import StaticCourseContent from "../StaticRoutes"
import DocViewer, {DocViewerRenderers} from "react-doc-viewer";
import FileViewer from "react-file-viewer";


const CourseContentTaskContainer = () => {
    const [content, setContent] = useState(null);

    const {id} = useParams();
    const {task_id} = useParams();

    const {Title} = Typography;

    const url = `/study_course/${id}/task/${task_id}`

    useEffect(() => {
        const ContentInfo = (Content) => {
            setContent(Content.content)
        }
        GetAnyInfo(ContentInfo, url)
    }, [url])

    console.log(StaticCourseContent.StaticCourseContent + `course_${id}/`)
    const headers = {
        'Access-Control-Allow-Origin': '*'
    }
    const ContentVisual = () => {
        if (content.content_type === 0 || content.content_type === 3) {
            return (<FileViewer
          fileType={'pdf'}
          filePath={'/static/course_content/' + `course_${id}/` + content.content_path}
        />)
            // return (<DocViewer pluginRenderers={DocViewerRenderers} documents={[{uri: '/static/course_content/' + `course_${id}/` + content.content_path}]} />)
        } else if (content.content_type === 2) {
            return (<ReactPlayer url={StaticCourseContent.StaticCourseContent + `course_${id}/` + content.content_path}
            controls={true}/>)
        }
    }

    return (
        content?
        <div>
            <Title>
                {content.content_name}
            </Title>
            <Title level={3}>
                {content.content_description}
            </Title>
            <ContentVisual/>
        </div>
            :
            <></>
    )
};

export default CourseContentTaskContainer;