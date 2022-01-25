import json
import os
import re

from Util.Annotation import rpcApi
from Util.RpcResult import RpcResult
from Util.util import suffixToPatternType, removeAudio, addTag, patternTypeToSuffix

patternToName = {"Gaussian noise": "gaussian_white_noise", "Sound level": "sound_level",
                 "Animal": "animal", "Source-ambiguous\nsounds": "source_ambiguous_sounds",
                 "Natural sounds": "natural_sounds", "Sound of things": "sound_of_things",
                 "Human sounds": "human_sounds", "Music": "music"}

nameToPattern = {"gaussian_white_noise": "Gaussian noise", "sound_level": "Sound level", "animal": "Animal",
                 "source_ambiguous_sounds": "Source-ambiguous\nsounds", "natural_sounds": "Natural sounds",
                 "sound_of_things": "Sound of things", "human_sounds": "Human sounds", "music": "Music"}


@rpcApi()
def getNoisePatternSummary(dataset):
    """
    获取某个数据集扰动大类的详情
    :param dataset:
    :return:
    """
    path = "D:/AudioSystem/NoiseAudio/" + dataset + "/clips"
    summary = {}
    for file in os.listdir(path):
        for key, value in patternToName.items():
            if value in file:
                if key in summary.keys():
                    summary[key] = summary[key] + 1
                else:
                    summary[key] = 1
                break
    sorted(summary)
    return RpcResult.ok(json.dumps(summary, ensure_ascii=False))


@rpcApi()
def getNoisePatternDetail(dataset, patternType):
    """
    获取某个数据集某个扰动大类的具体扰动类型详情
    :param dataset:
    :param patternType:
    :return:
    """
    path = "D:/AudioSystem/NoiseAudio/" + dataset + "/clips"
    summaryDetail = {}
    name = patternToName[patternType]
    for file in os.listdir(path):
        if name in file:
            if name == "gaussian_white_noise":
                pattern = name
            else:
                beg = file.index(name) + len(name) + 1
                end = file.index(".")
                pattern = file[beg:end]
            if pattern in summaryDetail.keys():
                summaryDetail[pattern] = summaryDetail[pattern] + 1
            else:
                summaryDetail[pattern] = 1
    sorted(summaryDetail)
    return RpcResult.ok(json.dumps(summaryDetail, ensure_ascii=False))


@rpcApi()
def getAudioSetPattern(dataset):
    """
    获取某个数据集每条音频的扰动详情
    :param dataset:
    :return:
    """
    path = "D:/AudioSystem/NoiseAudio/" + dataset + "/clips/"
    audioSetPattern = []
    key = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            temp = {"key": key}
            key += 1
            num = re.findall("\\d+", file)[0]
            temp["name"] = file[0:file.find(num) + len(num)] + ".mp3"
            if "gaussian_white_noise" in file:
                temp["pattern"] = nameToPattern["gaussian_white_noise"]
                temp["patternType"] = suffixToPatternType("gaussian_white_noise")
            else:
                temp["pattern"] = nameToPattern[file[file.find(num) + len(num) + 1:file.rfind("_")]]
                temp["patternType"] = suffixToPatternType(file[file.rfind("_") + 1:file.find(".")])
            audioSetPattern.append(temp)
    return RpcResult.ok(json.dumps(audioSetPattern, ensure_ascii=False))


@rpcApi()
def removeFormerAudio(dataset, audioName, pattern, patternType=None):
    path = "D:/AudioSystem/NoiseAudio/" + dataset + "/clips/"
    audioName = addTag(audioName, patternToName[pattern])
    if patternType is not None:
        audioName = addTag(audioName, patternTypeToSuffix(patternType))
    removeAudio(path, audioName)
    return RpcResult.ok("")


if __name__ == "__main__":
    pass
