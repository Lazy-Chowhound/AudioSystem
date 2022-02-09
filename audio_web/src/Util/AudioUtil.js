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

function getAudioAddress(dataset, audioName) {
    return baseUrl + "/Audio/" + dataset + "/clips/" + audioName
}

function getNoiseAudioAddress(dataset, audioName) {
    return baseUrl + "/NoiseAudio/" + dataset + "/clips/" + audioName
}

export {getAudioSet, getAudioAddress, getNoiseAudioAddress}