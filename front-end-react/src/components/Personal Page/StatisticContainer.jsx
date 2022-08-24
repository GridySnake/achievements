import React from "react";
import {Statistic, Tooltip} from "antd";

import styles from '../css/StatisticsContainer.module.css'

const StatisticContainer = ({action=null, title, values, icon, setLikeColor=null, setDislikeColor=null,
                                setRecommendColor=null, color=null, statical=null, setLike=null,
                            setDislike=null, setRecommend=null}) => {



    if (action !== null){
        if (setLikeColor !== null && !action[0]) {
            setLikeColor("#00ee00")
            color = "#00ee00"
            setLike(false)
        }
        if (setDislikeColor !== null && !action[1]) {
            setDislikeColor("#00ee00")
            color = "#00ee00"
            setDislike(false)
        }
        if (setRecommendColor !== null && !action[2]) {
            setRecommendColor("#00ee00")
            color = "#00ee00"
            setRecommend(false)
        }
    }


    return (
        statical?
                <Tooltip title={title}>
                    <Statistic value={values} prefix={icon}/>
                </Tooltip>
            :
            <Tooltip title={title}>
                <Statistic value={values} prefix={icon}
                       style={{background: color}} />
            </Tooltip>
    )
}

export default StatisticContainer;