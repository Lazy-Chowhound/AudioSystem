import json
import os

import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Util.Annotation import rpcApi
from Util.AudioUtil import *
from Util.RpcResult import RpcResult


@rpcApi
def getAudio(dataset, page, pageSize):
    Audio = []
    AudioList = getAudioList(dataset)
    Audio.append({'total': len(AudioList)})
    for i in range((int(page) - 1) * int(pageSize),
                   min(int(page) * int(pageSize), len(AudioList))):
        AudioProperty = getAudioProperty(dataset, AudioList[i])
        AudioProperty['key'] = i + 1
        Audio.append(AudioProperty)
    return RpcResult.ok(json.dumps(Audio, ensure_ascii=False))


def getAudioProperty(dataset, audioName):
    """
    获取某条音频所有属性
    :param dataset: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :return:
    """
    audio = getAudioSetClipPath(dataset) + audioName
    audioProperty = {}
    detail = getAudioDetail(dataset, audioName)
    audioProperty['name'] = audioName
    audioProperty['size'] = str(getDuration(audio)) + "秒"
    audioProperty['channel'] = "单" if getChannels(audio) == 1 else "双"
    audioProperty['sampleRate'] = str(getSamplingRate(audio)) + "Hz"
    audioProperty['bitDepth'] = str(getBitDepth(audio)) + "bit"
    audioProperty['content'] = detail['sentence']
    return audioProperty


def getAudioList(dataset):
    """
    获取目录下所有音频文件名
    :param dataset: cv-corpus-arabic
    :return:
    """
    path = getAudioSetClipPath(dataset)
    audioList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp3':
                audioList.append(file)
    return audioList


def getAudioDetail(dataset, audioName):
    """
    获取指定音频的详情
    :param dataset: cv-corpus-chinese
    :param audioName:
    :return:
    """
    path = getAudioSetPath(dataset)
    files = ['validated.tsv', 'invalidated.tsv', 'other.tsv']
    detail = {}
    for file in files:
        train = pd.read_csv(os.path.join(path, file), sep='\t', header=0)
        for index, row in train.iterrows():
            if audioName in row['path']:
                detail['id'] = index
                for item in row.items():
                    detail[item[0]] = item[1]
                break
    return detail


# 波形图、振幅
@rpcApi
def getWaveForm(dataset, audioName):
    audio = os.path.join(getAudioSetClipPath(dataset), audioName)
    sig, sr = librosa.load(audio, sr=None)
    plt.figure(figsize=(8, 5))
    librosa.display.waveshow(sig, sr=sr)
    plt.ylabel('Amplitude')
    savingPath = "D:/AudioSystem/WaveImage/" + audioName + ".jpg"
    plt.savefig(savingPath)
    return RpcResult.ok(savingPath)


# Mel频谱图
@rpcApi
def getMelSpectrum(dataset, audioName):
    audio = os.path.join(getAudioSetClipPath(dataset), audioName)
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
    return RpcResult.ok(savingPath)


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
@rpcApi
def removeImage(path):
    os.remove(path)
    return RpcResult.ok("Image removed")


if __name__ == '__main__':
    pass
