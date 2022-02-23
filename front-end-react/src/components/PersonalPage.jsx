import React, {useState, useEffect} from "react";
import { Image } from "antd";
import GetPersonalPageInfo from "../api/Api";
import StaticAvatars from "./StaticRoutes";

// const {Title} = Typography;
const PersonalPageContainer = () => {

    const [PersonalPage, setPersonalPage] = useState(null);
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        GetPersonalPageInfo(setPersonalPage)
    }, [setPersonalPage])

    return (
        PersonalPage ?
            <div>
                <Image
                    preview={{visible: false}}
                    width={200}
                    src={StaticAvatars.StaticAvatars + PersonalPage.href[0]}
                    onClick={() => setVisible(true)}
                />
                <div style={{ display: 'none' }}>
                    <Image.PreviewGroup preview={{ visible, onVisibleChange: vis => setVisible(vis) }}>
                    {PersonalPage.href.map((avatar) => {
                        return <Image src={StaticAvatars.StaticAvatars + avatar}/>
                    })
                    }
                    </Image.PreviewGroup>
                </div>
        </div>
         :
            <></>
    )
}

export default PersonalPageContainer