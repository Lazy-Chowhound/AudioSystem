import sendGet from "./axios";
import baseUrl from "./url";

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
    return baseUrl + "/Audio/" + dataset + "/clips/" + audioName
}

function getNoiseAudioUrl(dataset, audioName) {
    return baseUrl + "/NoiseAudio/" + dataset + "/clips/" + audioName
}

function getImageUrl(path){
    return path.replace("D:/AudioSystem", baseUrl)
}

export {getAudioSet, getAudioUrl, getNoiseAudioUrl,getImageUrl}