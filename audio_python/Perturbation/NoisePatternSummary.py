import json

from Dataset.DatasetList import getDatasetInstance
from Util.Annotation import rpcApi
from Util.RpcResult import RpcResult


@rpcApi
def get_pattern_summary(dataset):
    """
    获取某个数据集扰动大类的详情
    :param dataset: cv-corpus-chinese
    :return:
    """
    dataset_instance = getDatasetInstance(dataset)
    summary = dataset_instance.get_pattern_summary()
    return RpcResult.ok(json.dumps(summary, ensure_ascii=False))


@rpcApi
def get_pattern_type_summary(dataset, pattern):
    """
    获取某个数据集某个扰动大类的具体扰动类型详情
    :param dataset: cv-corpus-chinese
    :param pattern: Sound level
    :return:
    """
    dataset_instance = getDatasetInstance(dataset)
    summary_detail = dataset_instance.get_pattern_type_summary(pattern)
    return RpcResult.ok(json.dumps(summary_detail, ensure_ascii=False))
