import os


# 获取目录下所有音频文件名
def getAudioList(path):
    audioList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp3':
                audioList.append(file)
    return audioList
