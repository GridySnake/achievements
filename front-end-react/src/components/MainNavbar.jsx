import React from "react";
import {Link} from "react-router-dom";

const MainNavbar = () => {
    return (
        <div>
            <Link to="/user/0">Home</Link>
            <Link to="/subscribes">Subscribes</Link>
            <Link to="/goals">Goals</Link>
            <Link to="/achievements">Achievements</Link>
            <Link to="/communities">Communities</Link>
            <Link to="/courses">Courses</Link>
        </div>
    )
}

export default MainNavbar;