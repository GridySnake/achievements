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

const UploadStatic = (file, config, url, callback) => {
    console.log(file)
    axiosInstance.post(url, file, config)
    .then(({data})  => {
        callback(data.image_id)
    })
    .catch(({response}) => {
        console.log(response);
    })
}

const RemoveStaticImage = (image_id, callback) => {
    axiosInstance.post('/remove_image', image_id)
    .then(({data})  => {
        callback(data.response)
    })
    .catch(({response}) => {
        console.log(response);
    })
}

const RemoveStaticImageContent = (data, callback) => {
    axiosInstance.post('/remove_image_course_content', data)
    .then(({data})  => {
        callback(data.response)
    })
    .catch(({response}) => {
        console.log(response);
    })
}

export {UploadStatic, RemoveStaticImage, RemoveStaticImageContent}