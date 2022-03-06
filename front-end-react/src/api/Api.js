import axiosInstance from "./APIClient";

const GetPersonalPageInfo = async (setPersonalPage, id) => {
    try {
        const resp = await axiosInstance.get(`user/${id}`);
        console.log(resp.data);
        setPersonalPage(resp.data)
    } catch (err) {
        console.error(err);
    }
};

export default GetPersonalPageInfo