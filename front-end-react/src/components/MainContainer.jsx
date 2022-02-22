import React, { useState } from "react";
import { Menu, Row, Col } from 'antd';
import FormsContainer from "./FormsContainer";

const { SubMenu } = Menu;
const dropdownOpen = 0;
const formOpen = 1;

const MainContainer = () => {
    const [menuState, setMenuState] = useState(null);
    return (
        <Row>
            <Col span={6}>
                <Menu
                    style={{ width: 256 }}
                    mode="inline"
                    theme="dark"
                >
                    <SubMenu key="sub1" title="First menu">
                        <Menu.ItemGroup key="g1" title="Form">
                            <Menu.Item key="1"
                                        onClick={() => setMenuState(formOpen)}
                            >
                                Render form</Menu.Item>
                        <Menu.ItemGroup key="g2" title="Dropdown">
                            <Menu.Item key="2"
                                       onClick={() => setMenuState(dropdownOpen)}
                            >
                                Render dropdown</Menu.Item>
                        </Menu.ItemGroup>
                        </Menu.ItemGroup>
                    </SubMenu>
                </Menu>
            </Col>
            <Col span={18}>
                <FormsContainer menuState={menuState} />
            </Col>
        </Row>
    )
}

export default MainContainer