import axiosInstance from "./APIClient";

const GetAnyUserInfo = async (set, url) => {
    try {
        const resp = await axiosInstance.get(url);
        set(resp.data)
        console.log(resp.data);
    } catch (err) {
        console.error(err);
    }
};

const GetAnyUserInfoVT = async (set, url) => {
    try {
        const resp = await axiosInstance.get(url);
        set(resp.data)
        console.log(resp.data);
    } catch (err) {
        console.error(err);
    }
};

export {GetAnyUserInfo, GetAnyUserInfoVT};