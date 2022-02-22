import json

from Dataset.CommonVoiceDataset import CommonVoiceDataset
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
    summary = {}
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        summary = cvd.get_pattern_summary()
    return RpcResult.ok(json.dumps(summary, ensure_ascii=False))


@rpcApi
def get_pattern_detail(dataset, pattern):
    """
    获取某个数据集某个扰动大类的具体扰动类型详情
    :param dataset: cv-corpus-chinese
    :param pattern: Sound level
    :return:
    """

    summaryDetail = {}
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        summaryDetail = cvd.get_pattern_detail(pattern)
    return RpcResult.ok(json.dumps(summaryDetail, ensure_ascii=False))
