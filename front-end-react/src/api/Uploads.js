import axios from 'axios';
import axiosInstance from "./APIClient";

const UploadAvatar = (url, data, callback) => {
    axiosInstance.post()
        .then(({data}) => {
        callback(data.value)
    })
    .catch(({response}) => {
        console.log(response);
    })
}

const UploadStatic = (file, config, callback) => {
    console.log(file)
    axiosInstance.post('/upload_group_avatar', file, config)
    .then(({data})  => {
        callback(data.image_id)
    })
    .catch(({response}) => {
        console.log(response);
    })
}

export {UploadStatic}