import json

from Dataset.CommonVoiceDataset.CommonVoiceDataset import CommonVoiceDataset
from Dataset.TimitDataset.TimitDataset import TimitDataset
from Util.Annotation import rpcApi
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
    elif dataset == "timit":
        td = TimitDataset("timit")
        summary = td.get_pattern_summary()
    return RpcResult.ok(json.dumps(summary, ensure_ascii=False))


@rpcApi
def get_pattern_detail(dataset, pattern):
    """
    获取某个数据集某个扰动大类的具体扰动类型详情
    :param dataset: cv-corpus-chinese
    :param pattern: Sound level
    :return:
    """

    summary_detail = {}
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        summary_detail = cvd.get_pattern_detail(pattern)
    elif dataset == "timit":
        td = TimitDataset("timit")
        summary_detail = td.get_pattern_detail(pattern)
    return RpcResult.ok(json.dumps(summary_detail, ensure_ascii=False))
