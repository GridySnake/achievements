import axiosInstance from "./APIClient";


const makeAction = (url, parameter, callback) => {
    axiosInstance.post(url, parameter)
    .then(({data}) => {
        callback(data.value)
        console.log(data.value);
    })
    .catch(({response}) => {
        console.log(response);
    })
};

export default makeAction;