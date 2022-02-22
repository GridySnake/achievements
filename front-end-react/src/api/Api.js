import axiosInstance from "./APIClient";
import {useState, useEffect} from "react";

async function GetSubscribers() {

    const response = await axiosInstance.get('/user/0');
    console.log(response);

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
    // const [State, setState] = useState();
    // useEffect(() => {
    //     axiosInstance.get(apiUrl).then((response) => {
    //         const Subscribers = response.data;
    //         setState(Subscribers);
    //     });
    // }, [setState]);
    // return State
}
export default GetSubscribers