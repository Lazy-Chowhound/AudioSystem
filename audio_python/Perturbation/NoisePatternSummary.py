import json

from Util.Annotation import rpcApi
from Util.AudioUtil import *
from Util.RpcResult import RpcResult


@rpcApi
def get_pattern_summary(dataset):
    """
    获取某个数据集扰动大类的详情
    :param dataset: cv-corpus-chinese
    :return:
    """
    path = get_noise_audio_clips_path(dataset)
    summary = {}
    for file in os.listdir(path):
        for key, value in pattern_to_name.items():
            if value in file:
                if key in summary.keys():
                    summary[key] = summary[key] + 1
                else:
                    summary[key] = 1
                break
    sorted(summary)
    return RpcResult.ok(json.dumps(summary, ensure_ascii=False))


@rpcApi
def get_pattern_detail(dataset, pattern):
    """
    获取某个数据集某个扰动大类的具体扰动类型详情
    :param dataset: cv-corpus-chinese
    :param pattern: Sound level
    :return:
    """
    path = get_noise_audio_clips_path(dataset)
    summaryDetail = {}
    name = pattern_to_name[pattern]
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
def get_audio_clips_pattern(dataset):
    """
    获取某个数据集所有音频的扰动详情
    :param dataset: cv-corpus-chinese
    :return:
    """
    path = get_noise_audio_clips_path(dataset)
    audio_set_pattern = []
    key = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            pattern_info = {"key": key}
            key += 1
            num = re.findall("\\d+", file)[0]
            pattern_info["name"] = file[0:file.find(num) + len(num)] + ".mp3"
            patternTag = file[file.find(num) + len(num) + 1:file.find(".")]
            pattern_info["pattern"], pattern_info["patternType"] = get_pattern_info_from_name(patternTag)
            audio_set_pattern.append(pattern_info)
    return RpcResult.ok(json.dumps(audio_set_pattern, ensure_ascii=False))


@rpcApi
def remove_current_noise_audio_clip(dataset, audio_name, pattern, patternType=None):
    """
    删除现有的扰动音频
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :param pattern: Animal
    :param patternType: Wild animals
    :return:
    """
    path = get_noise_audio_clips_path(dataset)
    audio_name = add_tag(audio_name, pattern_to_name[pattern])
    if patternType is not None:
        audio_name = add_tag(audio_name, pattern_type_to_suffix(patternType))
    remove_audio(path, audio_name)
    return RpcResult.ok("")
