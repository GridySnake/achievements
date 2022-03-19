import React, {useEffect, useState} from "react";
import GetAnyUserInfo from "../api/GeneralApi";

const SubscribesContainer = () => {
    const [Subscribes, setSubscribes] = useState(null);
    useEffect(() => {
        GetAnyUserInfo(setSubscribes, '/subscribes')
    }, [setSubscribes])
    console.log(Subscribes)
    return (
        <div>
            1
        </div>
    )
};


export default SubscribesContainer;