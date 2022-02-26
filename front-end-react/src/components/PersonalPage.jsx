import React, {useState, useEffect} from "react";
import { Image } from "antd";
import GetPersonalPageInfo from "../api/Api";
import StaticAvatars from "./StaticRoutes";

// const {Title} = Typography;
const PersonalPageContainer = () => {

    const [User, setUser] = useState(null);
    const [Statistics, setStatistics] = useState(null);
    const [Posts, setPosts] = useState(null);
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        GetPersonalPageInfo(setUser, setStatistics, setPosts)
    }, [setUser, setStatistics, setPosts])

    // const
// const User = PersonalPageInfo[0]
    return (
        User ?

            <div>
                <Image
                    preview={{visible: false}}
                    width={200}
                    src={StaticAvatars.StaticAvatars + User.href[0]}
                    onClick={() => setVisible(true)}
                />
                <div style={{ display: 'none' }}>
                    <Image.PreviewGroup preview={{ visible, onVisibleChange: vis => setVisible(vis) }}>
                    {User.href.map((avatar) => {
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