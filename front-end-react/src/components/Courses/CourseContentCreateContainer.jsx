import type {InputRef, UploadProps} from 'antd';
import {Button, Form, Input, Popconfirm, Table, Space, Upload, Skeleton, Image} from 'antd';
import type { FormInstance } from 'antd/es/form';
import React, { useContext, useEffect, useRef, useState } from 'react';
import {InboxOutlined} from "@ant-design/icons";
import {useParams} from "react-router-dom";
import {RemoveStaticImageContent} from "../../api/AvatarAction";


const CourseContentCreateContainer =() => {
    // const inputRef = useRef<InputRef>(null);
    const {id} = useParams();
    const [content, setContent] = useState([]);
    const [remove, setRemove] = useState(null);
    const [count, setCount] = useState(3);
    const props: UploadProps = {
        name: 'file',
        action: `http://localhost:8082/upload_course_content/course_${id}`,
      onChange(info) {
        const { status } = info.file;
        if (status !== 'uploading') {
          console.log(info.file, info.fileList);
        }
        if (status === 'done') {
          content.push(info.file.xhr.response.split(': ')[1].split('}')[0])
            console.log(content)
        } else if (status === 'error') {
          console.log(`${info.file.name} file upload failed.`);
        }
      },
        onRemove(key) {
            const image_id = key.xhr.response.split(': ')[1].split('}')[0]
            setContent(content.filter(function(value, index, arr){
        return value !== image_id;
        }))
            RemoveStaticImageContent({image_id, id}, (data) => {
                setRemove(data)
            })
            console.log('Dropped files');
            },
        progress: {
            strokeColor: {
              '0%': '#108ee9',
              '100%': '#87d068',
            },
            strokeWidth: 3,
            format: percent => percent && `${parseFloat(percent.toFixed(2))}%`,
        },
    };
    const [data, setData] = useState([
  {
    key: 0,
    title: <Input type='text'/>,
    description: <Input type='text'/>,
    content: (<Upload.Dragger name="files" {...props}
                              headers={{'Access-Control-Allow-Origin': '*'}} withCredentials={true} maxCount={1}/>),
      chapter: <Input type='text'/>,
      subchapter: <Input type='text'/>
  }
]);
const Delete = (e) => {
    console.log(e)
    // console.log(e.nativeEvent.path[3].attributes[0].value)
    const rowKey = parseInt(e.nativeEvent.path[3].attributes[0].value)
    for (let value of data) {
        if (value.key === rowKey) {
            console.log(rowKey)
            if (data.indexOf(value) === data.length - 1) {
                console.log(data.pop())
            } else {
                console.log(data.splice(data.indexOf(value), 1))
            }
        }
    }
    }
    console.log(remove)
    const columns = [
  {
    title: "Title",
    dataIndex: "title",
    key: "title",
    render: (text) => <a>{text}</a>
  },
  {
    title: "Description",
    dataIndex: "description",
    key: "description",
      render: () => (<Input type="text"/>
      )
  },
  {
    title: "Content",
    dataIndex: "content",
    key: "content",
      render: () =>
          (<Upload.Dragger name="files" {...props}
                            headers={{'Access-Control-Allow-Origin': '*'}} withCredentials={true} maxCount={1}/>)
  },
  {
    title: "Chapter",
    key: "chapter",
    dataIndex: "chapter",
      render: () => (<Input type="text"/>
      )
  },
  {
    title: "Subchapter",
    key: "subchapter",
      dataIndex: "subchapter",
    render: () => (<Input type="text"/>
    )
  },
  {
    title: "Delete",
    key: "delete",
      dataIndex: "delete",
    render: () => (<Button onClick={e => Delete(e)}>Delete</Button>
    )
  }
];



const rowRef = useRef(null);

console.log(data)
const addRow = () => {
    const newData = {
    key: count+1,
    title: <Input type="text"/>,
    description: <Input type="text"/>,
    content: (<Upload.Dragger name="files" {...props}
                            headers={{'Access-Control-Allow-Origin': '*'}} withCredentials={true} maxCount={1}/>),
    chapter: <Input type="text"/>,
        subchapter: <Input type="text"/>,
        delete: <Button onClick={e => Delete(e)}>Delete</Button>
  }
    setData((pre) => {
      return [...pre, newData];
    })
    setCount(count+1)
}
    console.log(content)
    console.log('data', data)
  return (
      data && columns?
      <div>
    <Table
        pagination={false}
      columns={columns}
      dataSource={data}
      onRow={(_, index) => {
        if (index === data.length - 1) {
          return {
            ref: rowRef,
            onClick: () => {
              console.log(rowRef.current);
            }
          };
        }
        return {
          className: "hello"
        };
      }}
    />
          <Button onClick={addRow}>+</Button>
          </div>:
          <></>
  );
};

export default CourseContentCreateContainer;