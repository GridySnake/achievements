import axiosInstance from "./APIClient";

const GetPersonalPageInfo = async (setPersonalPage) => {
    try {
        const resp = await axiosInstance.get('/user/0');
        console.log(resp.data);
        setPersonalPage(resp.data)
    } catch (err) {
        console.error(err);
    }
};

export default GetPersonalPageInfo