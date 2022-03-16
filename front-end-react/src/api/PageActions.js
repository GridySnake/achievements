import axiosInstance from "./APIClient";


const makeAction = (url, owner) => {
    axiosInstance.post(url, owner)
    .then(({data}) => {
        console.log(data);
    })
    .catch(({response}) => {
        console.log(response);
    })
};

export {makeAction};