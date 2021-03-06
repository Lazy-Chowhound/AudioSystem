import json

import pymysql.cursors

from Util.Annotation import rpcApi
from Util.RpcResult import RpcResult


@rpcApi
def get_audio_sets_properties(user_name):
    """
    获取用户音频数据集及其所有属性
    :param user_name: 用户名
    :return:
    """
    audio_set = []
    for audio in get_audio_sets_list_from_db(user_name):
        audio_property = {}
        description = get_audio_set_description(audio)
        audio_property["key"] = description[0]
        audio_property["name"] = description[1]
        audio_property["language"] = description[2]
        audio_property["size"] = description[3]
        audio_property["hour"] = description[4]
        audio_property["people"] = description[5]
        audio_property["form"] = description[6]
        audio_property["description"] = description[7]
        audio_set.append(audio_property)
    return RpcResult.ok(json.dumps(audio_set, ensure_ascii=False))


@rpcApi
def get_audio_sets_list(user_name):
    """
    获取用户上传的数据集列表
    :param user_name: 用户名
    :return:
    """
    return RpcResult.ok(get_audio_sets_list_from_db(user_name))


def get_audio_sets_list_from_db(user_name):
    """
    获取用户数据集列表
    :return: ['cv-corpus-chinese','timit',....]
    """
    audio_list = []
    connect = pymysql.Connect(host="localhost", port=3306, user="root",
                              passwd="061210", db="audioset", charset="utf8")
    cursor = connect.cursor()
    cursor.execute(
        "select audio.name from audio,datasethistory where audio.name = datasethistory.name "
        "and datasethistory.user='%s'" % (user_name,))
    for item in cursor.fetchall():
        audio_list.append(item[0])
    cursor.close()
    connect.close()
    return audio_list


def get_audio_set_description(dataset):
    """
    从数据库获取数据集属性
    :param dataset: cv-corpus-chinese
    :return:
    """
    connect = pymysql.Connect(host="localhost", port=3306, user="root",
                              passwd="061210", db="audioset", charset="utf8")
    cursor = connect.cursor()
    cursor.execute(
        "select id,name,language,size,hour,people,form,description from audio where name = '%s'" % (dataset,))
    description = cursor.fetchone()
    cursor.close()
    connect.close()
    return description
