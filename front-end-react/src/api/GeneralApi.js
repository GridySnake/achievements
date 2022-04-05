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

const CreateUserChat = (data, callback) => {
    axiosInstance.post('/create_user_chat', data)
    .then(({data}) => {
        callback(data.chat_id)
    })
    .catch(({response}) => {
        console.log(response);
    })
};

const GetCitiesByCountry = async (data, set) => {
    try {
        const resp = await axiosInstance.get(`/get_cities_by_country/${data}`);
        set(resp.data)
        console.log(resp.data)
    } catch (err) {
        console.error(err);
    }
};

export {GetAnyUserInfo, CreateUserChat, GetCitiesByCountry};