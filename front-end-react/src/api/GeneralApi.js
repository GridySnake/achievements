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

export {GetAnyUserInfo, CreateUserChat};