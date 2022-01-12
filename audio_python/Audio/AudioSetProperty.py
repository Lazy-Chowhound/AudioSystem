import json
import os

import pymysql.cursors


# 获取所有音频数据集及其所有属性
def getAudioSet():
    AudioSet = []
    path = r"D:\AudioSystem\Audio"
    for audio in getAudioSetList(path):
        audioProperty = {}
        description = getAudioDescription(audio)
        audioProperty['key'] = description[0]
        audioProperty['name'] = description[1]
        audioProperty['language'] = description[2]
        audioProperty['size'] = description[3]
        audioProperty['hour'] = description[4]
        audioProperty['people'] = description[5]
        audioProperty['form'] = description[6]
        audioProperty['distribution'] = description[7]
        AudioSet.append(audioProperty)
    return json.dumps(AudioSet, ensure_ascii=False)


# 获取目录下的音频数据集
def getAudioSetList(path):
    audioSetList = []
    for file in os.listdir(path):
        filePath = os.path.join(path, file)
        if os.path.isdir(filePath):
            audioSetList.append(file)
    return audioSetList


# 从数据库获取数据集属性
def getAudioDescription(AudioSetName):
    connect = pymysql.Connect(host='localhost', port=3306, user='root',
                              passwd='061210', db='audioset', charset='utf8')
    cursor = connect.cursor()
    cursor.execute(
        "select id,name,language,size,hour,people,form,distribution from audio where name = '%s'" % (AudioSetName,))
    description = cursor.fetchone()
    cursor.close()
    connect.close()
    return description
