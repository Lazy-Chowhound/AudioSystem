import baseUrl from "./url";

const datasetPath = baseUrl + "/Audio/"

const clips_path = new Map([["cv-corpus-chinese", datasetPath + "cv-corpus-chinese/clips/"],
    ["timit", datasetPath + "timit/lisa/data/timit/raw/TIMIT/TRAIN/"]])

export {clips_path}