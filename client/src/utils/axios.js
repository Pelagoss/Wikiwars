import axios from "axios";
import {emitter} from "@/utils/index.js";

const myAxios = axios.create();

myAxios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;

myAxios.interceptors.request.use(function (config) {
    if (config.url !== '/login') {
        config.headers.set('Authorization', 'Bearer '+localStorage.getItem('token'));
    }

    return config;
}, function (error) {
    // Do something with request error
    return Promise.reject(error);
});

myAxios.interceptors.response.use(r => r, (error) => {
    if (!error.response) {
        return Promise.reject(error);
    }

    if (error.response.status === 401) {
        emitter.$emit('unAuthorized', error);
    }

    return Promise.reject(error);
});

export const $axios = myAxios;