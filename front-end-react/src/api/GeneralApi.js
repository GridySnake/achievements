import axiosInstance from "./APIClient";


const GetAnyUserInfo = async (set, url) => {
    try {
        const resp = await axiosInstance.get(url);
        console.log(resp.data);
        set(resp.data)
    } catch (err) {
        console.error(err);
    }
};

export default GetAnyUserInfo;