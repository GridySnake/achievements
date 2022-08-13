import React from "react";
import makeAction from "../../api/PageActions";
import {useNavigate, useParams} from "react-router";

const AchievementQRVerifyContainer = () => {
    const {qr} = useParams();
    const navigate = useNavigate();

    makeAction('/verify_achievement_qr', {'qr_value': qr, 'user_type': 0}, (value) => {
                navigate(`/achievement/${value.achievement_id}`)
        })


    return <></>
}

export default AchievementQRVerifyContainer;