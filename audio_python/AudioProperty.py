import json
import os
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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


def getAudioProperty(path, audioName):
    """
    获取音频所有属性
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/
    :param audioName:
    :return:
    """
    audio = path + "clips/" + audioName
    audioProperty = {}
    detail = getAudioDetail(path, audioName)
    audioProperty['name'] = audioName
    audioProperty['size'] = str(getDuration(audio)) + "秒"
    audioProperty['channel'] = "单" if getChannels(audio) == 1 else "双"
    audioProperty['sampleRate'] = str(getSamplingRate(audio)) + "Hz"
    audioProperty['bitDepth'] = str(getBitDepth(audio)) + "bit"
    audioProperty['content'] = detail['sentence']
    return audioProperty


def getAudioList(path):
    """
    获取目录下所有音频文件名
    :param path:D:/AudioSystem/Audio/cv-corpus-arabic/
    :return:
    """
    path += "clips/"
    audioList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp3':
                audioList.append(file)
    return audioList


def getAudioDetail(path, audioName):
    """
    获取指定音频的详情
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/
    :param audioName:
    :return:
    """
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
    savingPath = "D:/AudioSystem/WaveImage/" + audioName + ".jpg"
    plt.savefig(savingPath)
    return savingPath


# Mel频谱图
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
    savingPath = "D:/AudioSystem/SpectrumImage/" + audioName + ".jpg"
    plt.savefig(savingPath)
    return savingPath


# 音频的采样率
def getSamplingRate(audio):
    samplingRate = librosa.get_samplerate(audio)
    return samplingRate


# 音频时长
def getDuration(audio):
    sig, sr = librosa.load(audio, sr=None)
    return round(librosa.get_duration(sig, sr), 2)


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
