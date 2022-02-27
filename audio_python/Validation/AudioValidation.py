import json
import os

from Dataset.DatasetList import get_dataset_instance
from Util.Annotation import rpcApi
from Util.AudioUtil import MODEL_PATH
from Util.RpcResult import RpcResult


@rpcApi
def get_models():
    """
    获取所有模型
    :return:
    """
    model_list = []
    for model in os.listdir(MODEL_PATH):
        model_list.append(model)
    return RpcResult.ok(json.dumps(model_list, ensure_ascii=False))


@rpcApi
def get_validation_results_by_page(dataset, model_name, page, page_size):
    """
    获取验证内容
    :param dataset:
    :param model_name:
    :param page:
    :param page_size:
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    if not dataset_instance.load_model(model_name):
        return RpcResult.error("模型不存在，请选择正确的模型")
    results = dataset_instance.get_validation_results_by_page(page, page_size)
    return RpcResult.ok(json.dumps(results, ensure_ascii=False))
