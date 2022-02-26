import React from "react";
import StaticAvatars from "../StaticRoutes";
import {Image} from "antd";

const AvatarsContainer = (User, setVisible, visible, setAvatar) => {
    setAvatar(
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
                    })}
                </Image.PreviewGroup>
            </div>
        </div>
    )
}

export default AvatarsContainer