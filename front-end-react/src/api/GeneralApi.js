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

const GetSubspheresBySphere = async (data, set) => {
    try {
        const resp = await axiosInstance.get(`/get_subspheres_by_sphere/${data}`);
        set(resp.data)
        console.log(resp.data)
    } catch (err) {
        console.error(err);
    }
};

const GetConditionsByGroup = async (data, set) => {
    try {
        const resp = await axiosInstance.get(`/get_conditions_by_group/${data}`);
        set(resp.data)
        console.log(resp.data)
    } catch (err) {
        console.error(err);
    }
};

const GetConditionsByService = async (data, set) => {
    try {
        const resp = await axiosInstance.get(`/get_conditions_by_service/${data}`);
        set(resp.data)
        console.log(resp.data)
    } catch (err) {
        console.error(err);
    }
};

const GetConditionsByAggregation = async (data, set) => {
    try {
        const resp = await axiosInstance.get(`/get_conditions_by_aggregation/${data}`);
        set(resp.data)
        console.log(resp.data)
    } catch (err) {
        console.error(err);
    }
};

export {GetAnyUserInfo, CreateUserChat, GetCitiesByCountry, GetSubspheresBySphere, GetConditionsByGroup,
    GetConditionsByService, GetConditionsByAggregation};