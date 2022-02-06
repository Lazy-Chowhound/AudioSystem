import json

from Util.Annotation import rpcApi
from Util.AudioUtil import *
from Util.RpcResult import RpcResult


@rpcApi
def getNoisePatternSummary(dataset):
    """
    获取某个数据集扰动大类的详情
    :param dataset: cv-corpus-chinese
    :return:
    """
    path = getNoiseAudioSetClipPath(dataset)
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


@rpcApi
def getNoisePatternDetail(dataset, patternType):
    """
    获取某个数据集某个扰动大类的具体扰动类型详情
    :param dataset: cv-corpus-chinese
    :param patternType: Sound level
    :return:
    """
    path = getNoiseAudioSetClipPath(dataset)
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


@rpcApi
def getAudioSetPattern(dataset):
    """
    获取某个数据集每条音频的扰动详情
    :param dataset: cv-corpus-chinese
    :return:
    """
    path = getNoiseAudioSetClipPath(dataset)
    audioSetPattern = []
    key = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            patternInfo = {"key": key}
            key += 1
            num = re.findall("\\d+", file)[0]
            patternInfo["name"] = file[0:file.find(num) + len(num)] + ".mp3"
            patternTag = file[file.find(num) + len(num) + 1:file.find(".")]
            patternInfo["pattern"], patternInfo["patternType"] = getPatternInfoFromName(patternTag)
            audioSetPattern.append(patternInfo)
    return RpcResult.ok(json.dumps(audioSetPattern, ensure_ascii=False))


@rpcApi
def removeFormerAudio(dataset, audioName, pattern, patternType=None):
    """
    删除现有的扰动音频
    :param dataset: cv-corpus-chinese
    :param audioName: common_voice_zh-CN_18524189.mp3
    :param pattern: Animal
    :param patternType: Wild animals
    :return:
    """
    path = getNoiseAudioSetClipPath(dataset)
    audioName = addTag(audioName, patternToName[pattern])
    if patternType is not None:
        audioName = addTag(audioName, patternTypeToSuffix(patternType))
    removeAudio(path, audioName)
    return RpcResult.ok("")
