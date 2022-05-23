import json

import pymysql

from Dataset.DatasetList import get_dataset_instance
from Util.Annotation import rpcApi
from Util.RpcResult import RpcResult


@rpcApi
def get_models(user_name):
    """
    获取用户上传模型
    :param user_name: 用户名
    :return:
    """
    model_list = []
    connect = pymysql.Connect(host="localhost", port=3306, user="root",
                              passwd="061210", db="audioset", charset="utf8")
    cursor = connect.cursor()
    cursor.execute(
        "select name from modelhistory where user = '%s'" % (user_name,))
    for item in cursor.fetchall():
        model_list.append(item[0])
    cursor.close()
    connect.close()
    return RpcResult.ok(json.dumps(model_list, ensure_ascii=False))


@rpcApi
def get_validation_results_by_page(dataset, model_name, page, page_size):
    """
    按页获取验证内容
    :param dataset: 数据集名称
    :param model_name: 模型名
    :param page: 第几页
    :param page_size: 页大小
    :return:
    """
    try:
        dataset_instance = get_dataset_instance(dataset)
        if not dataset_instance.judge_model(model_name):
            return RpcResult.error("模型不适用于该数据集")
        dataset_instance.load_model(model_name)
        results = dataset_instance.get_validation_results_by_page(model_name, page, page_size)
        return RpcResult.ok(json.dumps(results, ensure_ascii=False))
    except Exception as e:
        return RpcResult.error(e)


@rpcApi
def get_validation_results_by_pattern(dataset, pattern, model_name, page, page_size):
    """
    按扰动类别获取验证内容
    :param dataset: 数据集名称
    :param pattern: 扰动类别
    :param model_name: 模型名
    :param page: 第几页
    :param page_size: 页大小
    :return:
    """
    try:
        dataset_instance = get_dataset_instance(dataset)
        if not dataset_instance.judge_model(model_name):
            return RpcResult.error("模型不适用于该数据集")
        dataset_instance.load_model(model_name)
        results = dataset_instance.get_validation_results_by_pattern(pattern, model_name, page, page_size)
        return RpcResult.ok(json.dumps(results, ensure_ascii=False))
    except Exception as e:
        return RpcResult.error(e)
