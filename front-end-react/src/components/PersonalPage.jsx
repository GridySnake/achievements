// import React, {useState, useEffect} from "react";
// import {Typography} from "antd";
import GetSubscribers from "../api/Api";
// import axiosInstance from "../api/APIClient";

// const {Title} = Typography;

const PersonalPage = () => {
    // console.log(1)
    const { subscribers } = GetSubscribers('/user/0')
    console.log(subscribers)

    return (
        subscribers &&
        <div>
            <table>
                <thead>
                    <tr>
                        <th>user_id</th>
                        <th>name</th>
                        <th>surname</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        subscribers.map((subscriber) =>
                            <tr key={subscriber.user_id}>
                                <td>{subscriber.user_id}</td>
                                <td>{subscriber.name}</td>
                                <td>{subscriber.surname}</td>
                            </tr>
                        )
                    }
                </tbody>
            </table>
      </div>
    )
}

export default PersonalPage