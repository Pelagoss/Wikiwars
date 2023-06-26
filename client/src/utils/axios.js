import axios from "axios";
import {emitter} from "./index.js";

const myAxios = axios.create();

myAxios.defaults.baseURL = "http://127.0.0.1:5000/api";

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
    if (error.response.status === 401) {
        emitter.$emit('unAuthorized', error);
    }

    return Promise.reject(error);
});

export const $axios = myAxios;