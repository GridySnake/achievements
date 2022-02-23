import axiosInstance from "./APIClient";
import {useState, useEffect} from "react";

// async function GetSubscribers() {
//     return await axiosInstance.get('/user/0');
// }
const GetPersonalPageInfo = async (setPersonalPage) => {
    try {
        const resp = await axiosInstance.get('/user/0');
        console.log(resp.data);
        setPersonalPage(resp.data)
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