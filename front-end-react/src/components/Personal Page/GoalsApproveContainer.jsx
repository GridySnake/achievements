import { MinusOutlined, PlusOutlined } from '@ant-design/icons';
import { Button, Progress } from 'antd';
import React, {useState} from "react";
import makeAction from "../../api/PageActions";

const GoalsApproveContainer = (props) => {
    const [isApproved, setIsApproved] = useState(props.is_approved);
    const [approveData, setApproveData] = useState(props.approve);
    const id = props.id
    console.log(approveData)

    const increase = (achievement_id, user_id) => {
        console.log(achievement_id)
        makeAction('/approve', {'achievement_id': achievement_id, 'user_id': user_id}, (value) => {
            setIsApproved(value.is_approved)
            setApproveData(value.approve)
        })
      };

    const decline = (achievement_id, user_id) => {
        makeAction('/disapprove', {'achievement_id': achievement_id, 'user_id': user_id}, (value) => {
            setIsApproved(value.is_approved)
            setApproveData(value.approve)
        })
    };

    return (
        props?
            <div>
                {approveData.map((goal, index) => {
                    return (
                        <>
                            <Progress type="circle" percent={goal.current_percentage}/>
                            {props.owner ?
                                <></>
                                :
                                <Button.Group>
                                    <Button onClick={() => decline(goal.achievement_id, id)} icon={<MinusOutlined/>}
                                            disabled={!isApproved[index].approved}/>
                                    <Button onClick={() => increase(goal.achievement_id, id)} icon={<PlusOutlined/>}
                                            disabled={isApproved[index].approved}/>
                                </Button.Group>
                            }
                        </>
                    )
                })
                }
            </div>
            :
            <></>
    );
}

export default GoalsApproveContainer;