import React, { useState } from "react";
import makeAction from "../../api/PageActions";
import {useNavigate, useParams} from "react-router";


const AchievementGeoContainer = () => {

    const [lat, setLat] = useState(null);
    const [lon, setLon] = useState(null);
    const [accuracy, setAccuracy] = useState(null);
    // const {achievement_id} = useParams();
    // const navigate = useNavigate();
    // console.log(achievement_id)

    const options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0,
    };

    const success = (pos) => {
        const crd = pos.coords;

        setLat(crd.latitude);
        setLon(crd.longitude);
        setAccuracy(crd.accuracy);
    }

    const errors = (err) => {
        console.warn(`ERROR(${err.code}): ${err.message}`);
    }
    console.log(navigator.geolocation.getCurrentPosition(success))
    const Geolocation = () => {
        if (navigator.geolocation) {
            navigator.permissions
                .query({ name: "geolocation" })
                .then(function (result) {
                    if (result.state === "granted") {
                        navigator.geolocation.getCurrentPosition(success);
                    } else if (result.state === "prompt") {
                        navigator.geolocation.getCurrentPosition(success, errors, options);
                    } else if (result.state === "denied") {
                        console.log('denied')
                    }
                });
        } else {
            alert("Sorry Not available!");
        }
    }

    console.log(lat, lon)

    // makeAction('/verify_achievement_geo', {'achievement_id': achievement_id, 'lat': lat, 'lon': lon,
    //     'accuracy': accuracy, 'user_type': 0}, (value) => {
    //             navigate(`/achievement/${value.achievement_id}`)
    //     })

    return (<>{Geolocation}{lat}{lon}{accuracy}</>)
}

export default AchievementGeoContainer;