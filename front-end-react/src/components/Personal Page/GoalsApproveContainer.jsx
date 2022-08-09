import { MinusOutlined, PlusOutlined } from '@ant-design/icons';
import { Button, Progress } from 'antd';
import React, {useState} from "react";
import makeAction from "../../api/PageActions";

const GoalsApproveContainer = (props) => {
    const [isApproved, setIsApproved] = useState(props.is_approved);
    const [approveData, setApproveData] = useState(props.approve);
    const [isApprovedGot, setIsApprovedGot] = useState(props.is_approved_got);
    const [approveDataGot, setApproveDataGot] = useState(props.approve_got);
    const id = props.id

    const increase = (achievement_id, user_id) => {
        makeAction('/approve', {'achievement_id': achievement_id, 'user_id': user_id}, (value) => {
            setIsApproved(value.is_approved)
            setApproveData(value.approve)
            setIsApprovedGot(value.is_approved_got)
            setApproveDataGot(value.approve_got)
        })
      };

    const decline = (achievement_id, user_id, type) => {
        makeAction('/disapprove', {'achievement_id': achievement_id, 'user_id': user_id, 'type': type,
            'user_type': 0},
            (value) => {
            setIsApproved(value.is_approved)
            setApproveData(value.approve)
            setIsApprovedGot(value.is_approved_got)
            setApproveDataGot(value.approve_got)
        })
    };

    return (
        id?
            <div>
                {approveData ?
                    <div>
                        <p>Goals</p>
                        {approveData.map((goal, index) => {
                            return (
                                <>
                                    <a href={`/achievement/${goal.achievement_id}`}>{goal.name}</a>
                                    <Progress type="circle" percent={goal.current_percentage}/>
                                    {props.owner ?
                                        <></>
                                        :
                                        <Button.Group>
                                            <Button onClick={() => decline(goal.achievement_id, id, false)}
                                                    icon={<MinusOutlined/>}
                                                    disabled={!isApproved[index].approved}/>
                                            <Button onClick={() => increase(goal.achievement_id, id)}
                                                    icon={<PlusOutlined/>}
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
                }
                {approveDataGot ?
                    <div>
                        <p>Achievements</p>
                        {approveDataGot.map((goal, index) => {
                            return (
                                <>
                                    <a href={`/achievement/${goal.achievement_id}`}>{goal.name}</a>
                                    <Progress type="circle" percent={goal.current_percentage}/>
                                    {props.owner ?
                                        <></>
                                        :
                                        <Button.Group>
                                            <Button onClick={() => decline(goal.achievement_id, id, true)}
                                                    icon={<MinusOutlined/>}
                                                    disabled={!isApprovedGot[index].approved}/>
                                            <Button onClick={() => increase(goal.achievement_id, id)}
                                                    icon={<PlusOutlined/>}
                                                    disabled={isApprovedGot[index].approved}/>
                                        </Button.Group>
                                    }
                                </>
                            )
                        })
                        }
                    </div>
                :
                <></>
                }
            </div>
            :
            <></>
    );
}

export default GoalsApproveContainer;