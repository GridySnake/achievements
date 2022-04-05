import axiosInstance from "./APIClient";

const SendMessage = (data, callback) => {
    axiosInstance.post('/send_message', data)
    .then(({data}) => {
        callback(data.value)
    })
    .catch(({response}) => {
        console.log(response);
    })
};

const CreateGroupChat = (data, callback) => {
    axiosInstance.post('/create_group_chat', data)
    .then(({data}) => {
        callback(data.chat_id)
    })
    .catch(({response}) => {
        console.log(response);
    })
};

const AddChatMembers = (data, callback) => {
    axiosInstance.post('/add_chat_member', data)
    .then(({data}) => {
        callback(data.value)
    })
    .catch(({response}) => {
        console.log(response);
    })
};

const RemoveChatMembers = (data, callback) => {
    axiosInstance.post('/remove_chat_member', data)
    .then(({data}) => {
        callback(data.value)
    })
    .catch(({response}) => {
        console.log(response);
    })
};

const ChangeUserSettings = (data, callback) => {
    axiosInstance.post('/user_info', data)
    .then(({data}) => {
        callback(data.response)
    })
    .catch(({response}) => {
        console.log(response);
    })
};

export {SendMessage, CreateGroupChat, AddChatMembers, RemoveChatMembers, ChangeUserSettings};