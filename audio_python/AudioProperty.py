import json
import os
import librosa.display
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pydub import AudioSegment


def getAudio(AudioSetName, page, pageSize):
    Audio = []
    path = "D:/AudioSystem/Audio/" + AudioSetName + "/"
    AudioList = getAudioList(path)
    Audio.append({'total': len(AudioList)})
    for i in range((int(page) - 1) * int(pageSize) - int(page) + 1,
                   min(int(page) * int(pageSize) - int(page), len(AudioList))):
        AudioProperty = getAudioProperty(path, AudioList[i])
        AudioProperty['key'] = i + 1
        Audio.append(AudioProperty)
    return json.dumps(Audio, ensure_ascii=False)


# 获取音频所有属性
# path形如D:/AudioSystem/Audio/cv-corpus-chinese/
def getAudioProperty(path, audioName):
    audio = path + "clips/" + audioName
    audioProperty = {}
    detail = getAudioDetail(path, audioName)
    audioProperty['name'] = audioName
    audioProperty['size'] = str(getDuration(audio)) + "秒"
    audioProperty['gender'] = "" if type(detail['gender']) == float else detail['gender']
    audioProperty['age'] = "" if type(detail['age']) == float else detail['age']
    audioProperty['channel'] = "单" if getChannels(audio) == 1 else "双"
    audioProperty['sampleRate'] = str(getSamplingRate(audio)) + "Hz"
    audioProperty['bitDepth'] = str(getBitDepth(audio)) + "bit"
    audioProperty['content'] = detail['sentence']
    return audioProperty


# 获取目录下所有音频文件名
# path形如D:/AudioSystem/Audio/cv-corpus-arabic/
def getAudioList(path):
    path += "clips/"
    audioList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp3':
                audioList.append(file)
    return audioList


# 获取指定音频的详情
# path形如D:/AudioSystem/Audio/cv-corpus-chinese/
def getAudioDetail(path, audioName):
    files = ['validated.tsv', 'invalidated.tsv', 'other.tsv']
    detail = {}
    for file in files:
        train = pd.read_csv(path + file, sep='\t', header=0)
        for index, row in train.iterrows():
            if audioName in row['path']:
                detail['id'] = index
                for item in row.items():
                    detail[item[0]] = item[1]
                break
    return detail


# 波形图、振幅
def getWaveForm(audioSetName, audioName):
    path = "D:/AudioSystem/Audio/" + audioSetName + "/"
    audio = path + "clips/" + audioName
    sig, sr = librosa.load(audio, sr=None)
    plt.figure(figsize=(8, 5))
    librosa.display.waveshow(sig, sr=sr)
    plt.ylabel('Amplitude')
    savingPath = "D:/AudioSystem/audio_java/src/main/resources/static/WaveImage/" + audioName + ".jpg"
    plt.savefig(savingPath)
    return savingPath


# Mel频谱图
# path形如D:/AudioSystem/Audio/cv-corpus-chinese/
def getMelSpectrum(audioSetName, audioName):
    path = "D:/AudioSystem/Audio/" + audioSetName + "/"
    audio = path + "clips/" + audioName
    sig, sr = librosa.load(audio, sr=None)
    S = librosa.feature.melspectrogram(y=sig, sr=sr)
    plt.figure(figsize=(8, 5))
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
                             y_axis='mel', fmax=8000, x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    savingPath = "D:/AudioSystem/audio_java/src/main/resources/static/SpectrumImage/" + audioName + ".jpg"
    plt.savefig(savingPath)
    return savingPath


# 音频的采样率
def getSamplingRate(audio):
    samplingRate = librosa.get_samplerate(audio)
    return samplingRate


# 音频时长
def getDuration(audio):
    sig, sr = librosa.load(audio, sr=None)
    return librosa.get_duration(sig, sr)


# 声道
def getChannels(audio):
    song = AudioSegment.from_mp3(audio)
    return song.channels


# 位深
def getBitDepth(audio):
    song = AudioSegment.from_mp3(audio)
    return song.sample_width * 8


# 删除图片
def removeImage(path):
    os.remove(path)
    return "Image removed"


if __name__ == '__main__':
    print(getAudio("cv-corpus-japanese", 1, 6))
