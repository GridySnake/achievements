import React, { useState } from "react";
import {Typography} from "antd";
const {Title} = Typography;
const defaultColor = "#eeee00"

const MainTitle = () => {
    const [color, setColor] = useState(defaultColor);
    return (
        <Title
            level={1}
            style={{color: color}}
            onClick={() => {
                if (color === defaultColor) {
                    setColor("#00ee00")
                } else{
                    setColor(defaultColor);
                }
            }}
        >
            Hello Kek
        </Title>
    )
}

export default MainTitle