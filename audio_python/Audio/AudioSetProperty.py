import json
import os

import pymysql.cursors

from Util.Annotation import rpcApi
from Util.RpcResult import RpcResult


@rpcApi
def getAudioSet():
    """
    获取所有音频数据集及其所有属性
    :return:
    """
    AudioSet = []
    projectPath = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    path = os.path.join(projectPath, "Audio/")
    for audio in json.loads(audioSetList(path)):
        audioProperty = {}
        description = getAudioDescription(audio)
        audioProperty["key"] = description[0]
        audioProperty["name"] = description[1]
        audioProperty["language"] = description[2]
        audioProperty["size"] = description[3]
        audioProperty["hour"] = description[4]
        audioProperty["people"] = description[5]
        audioProperty["form"] = description[6]
        audioProperty["distribution"] = description[7]
        AudioSet.append(audioProperty)
    return RpcResult.ok(json.dumps(AudioSet, ensure_ascii=False))


@rpcApi
def getAudioSetList(path):
    """
    获取目录下的音频数据集
    :param path: 路径
    :return:
    """
    return RpcResult.ok(audioSetList(path))


def audioSetList(path):
    """
    获取目录下的音频数据集
    :param path: 路径
    :return:
    """
    setList = []
    for file in os.listdir(path):
        filePath = os.path.join(path, file)
        if os.path.isdir(filePath):
            setList.append(file)
    return json.dumps(setList, ensure_ascii=False)


def getAudioDescription(dataset):
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
