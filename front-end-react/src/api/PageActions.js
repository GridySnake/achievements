import axiosInstance from "./APIClient";


const makeAction = (url, owner, callback) => {
    axiosInstance.post(url, owner)
    .then(({data}) => {
        callback(data.value)
        console.log(data.value);
    })
    .catch(({response}) => {
        console.log(response);
    })
};

export default makeAction;