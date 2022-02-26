import axiosInstance from "./APIClient";
import {useState, useEffect} from "react";

// async function GetSubscribers() {
//     return await axiosInstance.get('/user/0');
// }
const GetPersonalPageInfo = async (setUser, setStatistics, setPosts) => {
    try {
        const resp = await axiosInstance.get('/user/0');
        console.log(resp.data);
        setUser(resp.data['user'])
        setStatistics(resp.data['statistics'])
        setPosts(resp.data['posts'])
    } catch (err) {
        console.error(err);
    }
};
  //   const [appState, setAppState] = useState(
  //       {
  //           subscribers: null
  //       }
  // )
 // useEffect(() => {
 //    axiosInstance.get(apiUrl).then((resp) => {
 //      const subscribers = resp.data;
 //      setAppState({
 //      subscribers: subscribers
 //       });
 //    });
 //  }, [appState]);
 //        axiosInstance.get(apiUrl).then((response) =>

// }

export default GetPersonalPageInfo