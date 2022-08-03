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
    name: <Input type='text'/>,
    age: 32,
    address: (<Upload.Dragger name="files" {...props}
                              headers={{'Access-Control-Allow-Origin': '*'}} withCredentials={true} maxCount={1}/>)
  }
]);

    console.log(remove)
    const columns = [
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
    render: (text) => <a>{text}</a>
  },
  {
    title: "Age",
    dataIndex: "age",
    key: "age"
  },
  {
    title: "Address",
    dataIndex: "address",
    key: "address",
      render: () =>
          (<Upload.Dragger name="files" {...props}
                            headers={{'Access-Control-Allow-Origin': '*'}} withCredentials={true} maxCount={1}/>)
  },
  {
    title: "Tags",
    key: "tags",
    dataIndex: "tags",
      render: () =>
          (<Input type="text"/>
      )
  },
  {
    title: "Action",
    key: "action",
    render: (text, record) => (
      <Space size="middle">
        <a>Invite {record.name}</a>
        <a>Delete</a>
      </Space>
    )
  }
];


const rowRef = useRef(null);


// const data = [
//   {
//     key: "1",
//     name: "John Brown",
//     age: 32,
//     address: "New York No. 1 Lake Park",
//     tags: ["nice", "developer"]
//   },
//   {
//     key: "2",
//     name: "Jim Green",
//     age: 42,
//     address: "London No. 1 Lake Park",
//     tags: ["loser"]
//   },
//   {
//     key: "3",
//     name: "Joe Black",
//     age: 32,
//     address: "Sidney No. 1 Lake Park",
//     tags: ["cool", "teacher"]
//   }
// ]

console.log(data)
const addRow = () => {
    const newData = {
    key: count+1,
    name: <Input type="text"/>,
    age: 31,
    address: (<Upload.Dragger name="files" {...props}
                            headers={{'Access-Control-Allow-Origin': '*'}} withCredentials={true} maxCount={1}/>),
    tags: ["cool", "teacher1"]
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