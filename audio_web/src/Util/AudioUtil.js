import {sendGet} from "./axios";
import baseUrl from "./url";
import {clips_path, noise_clips_path} from "./Path";

async function getAudioSet() {
    const ops = []
    let error = null
    await sendGet("/audioSetsList", {}).then(res => {
        if (res.data.code === 400) {
            error = res.data.data
        } else {
            const audioList = JSON.parse(res.data.data)
            for (let i = 0; i < audioList.length; i++) {
                ops.push(audioList[i])
            }
        }
    }).catch(err => {
        error = err
    })
    return new Promise((resolve, reject) => {
        ops.length > 0 ? resolve(ops) : reject(error)
    })
}

function getAudioUrl(dataset, audioName) {
    return clips_path.get(dataset) + audioName
}

function getNoiseAudioUrl(dataset, audioName) {
    return noise_clips_path.get(dataset) + audioName
}

function getImageUrl(path) {
    return path.replace("D:/AudioSystem", baseUrl)
}

function formatTime(timestamp) {
    const moment = require('moment');
    return moment(+timestamp).format('YYYY-MM-DD HH:mm:ss')
}

function formatTimeStamp(time) {
    const moment = require('moment');
    return moment(time).valueOf()
}


export {getAudioSet, getAudioUrl, getNoiseAudioUrl, getImageUrl, formatTime,formatTimeStamp}