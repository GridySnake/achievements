import type {InputRef, UploadProps} from 'antd';
import {Button, Form, Input, Popconfirm, Table, Space, Upload, Skeleton, Image} from 'antd';
import type { FormInstance } from 'antd/es/form';
import { MenuOutlined } from '@ant-design/icons';
import React, { useContext, useEffect, useRef, useState } from 'react';
import {InboxOutlined} from "@ant-design/icons";
import { SortableContainer, SortableElement, SortableHandle } from 'react-sortable-hoc';
import { arrayMoveImmutable } from 'array-move';
import type { SortableContainerProps, SortEnd } from 'react-sortable-hoc';
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

    const DragHandle = SortableHandle(() => <MenuOutlined style={{ cursor: 'grab', color: '#999' }} />);
    const SortableItem = SortableElement((props: React.HTMLAttributes<HTMLTableRowElement>) => (
  <tr {...props} />
));
const SortableBody = SortableContainer((props: React.HTMLAttributes<HTMLTableSectionElement>) => (
  <tbody {...props} />
));
    const [data, setData] = useState([
  {
    key: 0,
      chapter: <Input type='text'/>,
      subchapter: <Input type='text'/>,
    title: <Input type='text'/>,
    description: <Input type='text'/>,
    content: (<Upload.Dragger name="files" {...props}
                              headers={{'Access-Control-Allow-Origin': '*'}} withCredentials={true} maxCount={1}/>),
      delete: <Button onClick={e => Delete(e)}>Delete</Button>
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
                setData(data.pop())
            } else if (data.length === 1) {
                setData([
  {index: 0,
    key: 0,
      chapter: <Input type='text'/>,
      subchapter: <Input type='text'/>,
    title: <Input type='text'/>,
    description: <Input type='text'/>,
    content: (<Upload.Dragger name="files" {...props}
                              headers={{'Access-Control-Allow-Origin': '*'}} withCredentials={true} maxCount={1}/>),
      delete: <Button onClick={e => Delete(e)}>Delete</Button>
  }
])
                } else {
                setData(data.splice(data.indexOf(value), 1))
            }
        }
    }
    console.log('new_data', data)
    }
    console.log(remove)
    const columns = [
        {
    title: 'Sort',
    dataIndex: 'sort',
    width: 30,
    className: 'drag-visible',
    render: () => <DragHandle />,
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
    title: "Delete",
    key: "delete",
      dataIndex: "delete",
    render: () => (<Button onClick={e => Delete(e)}>Delete</Button>
    )
  }
];
  const onSortEnd = ({ oldIndex, newIndex }: SortEnd) => {
    if (oldIndex !== newIndex) {
      const newData = arrayMoveImmutable(data.slice(), oldIndex, newIndex)
      console.log('Sorted items: ', newData);
      setData(newData);
    }
  };

  const DraggableContainer = (props: SortableContainerProps) => (
    <SortableBody
      useDragHandle
      disableAutoscroll
      helperClass="row-dragging"
      onSortEnd={onSortEnd}
      {...props}
    />
  );

  const DraggableBodyRow: React.FC<any> = ({ className, style, ...restProps }) => {
    // function findIndex base on Table rowKey props and should always be a right array index
    const index = data.findIndex(x => x.index === restProps['data-row-key']);
    return <SortableItem index={index} {...restProps} />;
  };


const rowRef = useRef(null);

console.log(data)
const addRow = () => {
    const newData = {
        index: data[data.length -1].index+1,
    key: count+1,
        chapter: <Input type="text"/>,
        subchapter: <Input type="text"/>,
    title: <Input type="text"/>,
    description: <Input type="text"/>,
    content: (<Upload.Dragger name="files" {...props}
                            headers={{'Access-Control-Allow-Origin': '*'}} withCredentials={true} maxCount={1}/>),

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
        components={{
        body: {
          wrapper: DraggableContainer,
          row: DraggableBodyRow,
        },
      }}
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