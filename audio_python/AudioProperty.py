import os
from AudioProcess import *


# 获取音频所有属性
# path形如D:/AudioSystem/Audio/cv-corpus-chinese/
def getAudioProperty(path, audioName):
    audioPath = path + "clips/"
    audioProperty = {}
    detail = getAudioDetail(path, audioName)
    audioProperty['name'] = audioName
    audioProperty['size'] = str(getDuration(audioPath, audioName)) + "秒"
    audioProperty['gender'] = detail['gender']
    audioProperty['age'] = detail['age']
    audioProperty['channel'] = "单" if getChannels(audioPath, audioName) == 1 else "双"
    audioProperty['sampleRate'] = str(getSamplingRate(audioPath, audioName)) + "Hz"
    audioProperty['bitDepth'] = str(getBitDepth(audioPath, audioName)) + "bit"
    audioProperty['content'] = detail['sentence']
    return audioProperty


# 获取目录下所有音频文件名
def getAudioList(path):
    audioList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp3':
                audioList.append(file)
    return audioList


if __name__ == '__main__':
    print(getAudioProperty("D:/AudioSystem/Audio/cv-corpus-chinese/", "common_voice_zh-CN_18524189.mp3"))
