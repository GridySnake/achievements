import axiosInstance from "./APIClient";

const SendMessage = (url, data, callback) => {
    axiosInstance.post(url, data)
    .then(({data}) => {
        callback(data.value)
    })
    .catch(({response}) => {
        console.log(response);
    })
};

export default SendMessage;