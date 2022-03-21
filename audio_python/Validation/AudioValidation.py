import json

import pymysql

from Dataset.DatasetList import get_dataset_instance
from Util.Annotation import rpcApi
from Util.RpcResult import RpcResult


@rpcApi
def get_models(user_name):
    """
    获取用户上传模型
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
    获取验证内容
    :param dataset:
    :param model_name:
    :param page:
    :param page_size:
    :return:
    """
    try:
        dataset_instance = get_dataset_instance(dataset)
        dataset_instance.load_model(model_name)
        results = dataset_instance.get_validation_results_by_page(page, page_size)
        return RpcResult.ok(json.dumps(results, ensure_ascii=False))
    except Exception as e:
        return RpcResult.error(e)
