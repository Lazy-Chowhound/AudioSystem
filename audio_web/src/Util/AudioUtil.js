import sendGet from "./axios";

async function getAudioSet() {
    const ops = []
    let error = null
    await sendGet("/audioSetList", {
        params: {
            path: "D:/AudioSystem/Audio/"
        }
    }).then(res => {
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

export default getAudioSet