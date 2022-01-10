import os.path
import librosa
import numpy as np
import soundfile
from util import *


def normalize(waveData):
    """
    将标准正态分布样本变更加标准化
    :param waveData: ndarray
    :return:
    """
    standardDeviation = np.std(waveData)
    return (waveData - np.mean(waveData)) / standardDeviation


def gaussian_white_noise(waveData, snr):
    """
    高斯白噪声
    :param snr:
    :param waveData:
    :return:
    """
    data_type = waveData[0].dtype
    P_signal = np.sum(abs(waveData) ** 2) / len(waveData)  # 信号功率
    P_noise = P_signal / 10 ** (snr / 10.0)  # 噪声功率
    noise = np.random.normal(0, 1, size=len(waveData))
    noise = normalize(noise)
    noiseAudio = waveData + noise * np.sqrt(P_noise)
    noiseAudio = noiseAudio.astype(data_type)
    return noiseAudio


def add_gaussian_white_noise(path, audioName):
    wavePath, waveName = trans_mp3_to_wav(path, audioName)
    sig, sr = librosa.load(wavePath + waveName, sr=None)
    noiseAudio = gaussian_white_noise(sig, snr=5)
    noiseWaveName = addTag(waveName, "gaussian_white_noise")
    soundfile.write(wavePath + noiseWaveName, noiseAudio, sr)
    trans_wav_to_mp3(wavePath, noiseWaveName)

    removeAudio(wavePath, waveName)
    removeAudio(wavePath, noiseWaveName)


def addTag(path, tag):
    pos = path.index(".")
    return path[0:pos] + "_" + tag + path[pos:]


def removeAudio(path, audioName):
    os.remove(path + audioName)


if __name__ == '__main__':
    add_gaussian_white_noise("D:/AudioSystem/Audio/cv-corpus-chinese/clips/",
                             "common_voice_zh-CN_18524189.mp3")
