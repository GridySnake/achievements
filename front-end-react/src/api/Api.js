import axiosInstance from "./APIClient";

const GetPersonalPageInfo = async (setPersonalPage, id) => {
    try {
        const resp = await axiosInstance.get(`user/${id}`);
        setPersonalPage(resp.data)
        console.log(resp.data);
    } catch (err) {
        console.error(err);
    }
};

export default GetPersonalPageInfo