import axios from "axios";
import baseUrl from "./url";

axios.defaults.withCredentials = true;

const axiosInstance = axios.create({
    baseURL: baseUrl,
})

axiosInstance.interceptors.request.use(config => {
    // 给请求头加Authorization的字段
    config.headers.Authorization = localStorage.getItem("token")
    return config
})

function sendGet(url, params = {}) {
    return new Promise((resolve, reject) => {
        axiosInstance.get(url, params).then(res => {
            resolve(res);
        }).catch(error => {
            reject(error.toString())
        })
    });
}

function sendFile(url, data = {}) {
    return new Promise((resolve, reject) => {
        axiosInstance.post(url, data).then(res => {
            resolve(res);
        }).catch(error => {
            reject(error.toString())
        })
    });
}

export {sendGet, sendFile}