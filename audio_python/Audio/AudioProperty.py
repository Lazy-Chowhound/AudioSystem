import json

import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Util.Annotation import rpcApi
from Util.AudioUtil import *
from Util.RpcResult import RpcResult


@rpcApi
def getAudio(dataset, page, pageSize):
    """
    分页获取音频及其属性
    :param dataset: cv-corpus-chinese
    :param page: 页数
    :param pageSize: 页面大小
    :return:
    """
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
    :param dataset: cv-corpus-chinese
    :param audioName: common_voice_zh-CN_18524189.mp3
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


@rpcApi
def getWaveForm(dataset, audioName):
    """
    生成波形图
    :param dataset: cv-corpus-chinese
    :param audioName: 音频名
    :return:
    """
    audio = os.path.join(getAudioSetClipPath(dataset), audioName)
    sig, sr = librosa.load(audio, sr=None)
    plt.figure(figsize=(8, 5))
    librosa.display.waveshow(sig, sr=sr)
    plt.ylabel('Amplitude')
    savingPath = "D:/AudioSystem/WaveImage/" + audioName + ".jpg"
    plt.savefig(savingPath)
    return RpcResult.ok(savingPath)


@rpcApi
def getMelSpectrum(dataset, audioName):
    """
    生成 Mel频谱图
    :param dataset: cv-corpus-chinese
    :param audioName: 音频名
    :return:
    """
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


def getSamplingRate(audio):
    """
    获取音频的采样率
    :param audio: 音频路径
    :return:
    """
    samplingRate = librosa.get_samplerate(audio)
    return samplingRate


def getDuration(audio):
    """
    获取音频时长
    :param audio: 音频路径
    :return:
    """
    sig, sr = librosa.load(audio, sr=None)
    return round(librosa.get_duration(sig, sr), 2)


def getChannels(audio):
    """
    获取声道
    :param audio: 音频路径
    :return:
    """
    song = AudioSegment.from_mp3(audio)
    return song.channels


def getBitDepth(audio):
    """
    获取位深
    :param audio: 音频路径
    :return:
    """
    song = AudioSegment.from_mp3(audio)
    return song.sample_width * 8


@rpcApi
def removeImage(path):
    """
    删除图片
    :param path: 路径
    :return:
    """
    os.remove(path)
    return RpcResult.ok("Image removed")
