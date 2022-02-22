import baseUrl from "./url";

const datasetPath = baseUrl + "/Audio/"
const noiseDatasetPath = baseUrl + "/NoiseAudio/"

const clips_path = new Map([["cv-corpus-chinese", datasetPath + "cv-corpus-chinese/clips/"],
    ["timit", datasetPath + "timit/lisa/data/timit/raw/TIMIT/TRAIN/"]])

const noise_clips_path = new Map([["cv-corpus-chinese", noiseDatasetPath + "cv-corpus-chinese/clips/"],
    ["timit", noiseDatasetPath + "timit/lisa/data/timit/raw/TIMIT/TRAIN/"]])

export {clips_path, noise_clips_path}