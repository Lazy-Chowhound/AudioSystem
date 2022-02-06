import json
import os

import pymysql.cursors

from Util.Annotation import rpcApi
from Util.AudioUtil import AUDIO_SETS_PATH
from Util.RpcResult import RpcResult


@rpcApi
def get_audio_sets_properties():
    """
    获取所有音频数据集及其所有属性
    :return:
    """
    audio_set = []
    path = AUDIO_SETS_PATH
    for audio in json.loads(audio_sets_list(path)):
        audio_property = {}
        description = get_audio_set_description(audio)
        audio_property["key"] = description[0]
        audio_property["name"] = description[1]
        audio_property["language"] = description[2]
        audio_property["size"] = description[3]
        audio_property["hour"] = description[4]
        audio_property["people"] = description[5]
        audio_property["form"] = description[6]
        audio_property["distribution"] = description[7]
        audio_set.append(audio_property)
    return RpcResult.ok(json.dumps(audio_set, ensure_ascii=False))


@rpcApi
def get_audio_sets_list(path):
    """
    获取目录下的音频数据集
    :param path: 路径
    :return:
    """
    return RpcResult.ok(audio_sets_list(path))


def audio_sets_list(path):
    """
    获取目录下的音频数据集
    :param path: 路径
    :return:
    """
    set_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            set_list.append(file)
    return json.dumps(set_list, ensure_ascii=False)


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
        "select id,name,language,size,hour,people,form,distribution from audio where name = '%s'" % (dataset,))
    description = cursor.fetchone()
    cursor.close()
    connect.close()
    return description


if __name__ == '__main__':
    get_audio_sets_properties()
