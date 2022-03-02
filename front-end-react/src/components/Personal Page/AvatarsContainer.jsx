import React from "react";
import StaticAvatars from "../StaticRoutes";
import {Image} from "antd";

const AvatarsContainer = ({user, visible, setVisible}) => {
    return (
        <div>
            <Image
                  preview={{visible: false}}
                  width={200}
                  src={StaticAvatars.StaticAvatars + user.href[0]}
                  onClick={() => setVisible(true)}
            />
            <div style={{ display: 'none' }}>
                <Image.PreviewGroup preview={{ visible: visible, onVisibleChange: vis => setVisible(vis) }}>
                    {user.href.map((avatar, inx) => {
                        console.log(StaticAvatars.StaticAvatars + avatar)
                        return <Image key={inx} src={StaticAvatars.StaticAvatars + avatar}/>
                    })}
                </Image.PreviewGroup>
            </div>
        </div>
    )
}

export default AvatarsContainer