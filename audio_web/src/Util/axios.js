import axios from "axios";
import baseUrl from "./url";

const axiosInstance = axios.create({
    baseURL: baseUrl
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

function sendFile(url,data={}){
    return new Promise((resolve, reject) => {
        axiosInstance.post(url, data).then(res => {
            resolve(res);
        }).catch(error => {
            reject(error.toString())
        })
    });
}

export {sendGet,sendFile}