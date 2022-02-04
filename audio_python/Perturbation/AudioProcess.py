import math
import random

import librosa
import numpy as np


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
    :param waveData: numpy数组
    :param snr:
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


def louder(wavData):
    """
    提高响度
    :param wavData: numpy数组
    :return:
    """
    return wavData * 5


def quieter(wavData):
    """
    降低响度
    :param wavData: numpy数组
    :return:
    """
    return wavData / 5


def changePitch(wavData, sr):
    """
    改变音高
    :param wavData:
    :param sr:
    :return:
    """
    pitch = random.randint(5, 10) * random.randrange(-1, 2, 2)
    noiseAudio = librosa.effects.pitch_shift(wavData, sr, n_steps=float(pitch))
    return noiseAudio


def addNoise(waveData, noiseData):
    audioLength = len(waveData)
    # 先使噪声长度大于等于音频，然后再截取成一样
    if len(waveData) > len(noiseData):
        noiseData = np.tile(noiseData, math.ceil(len(waveData) / len(noiseData)))
    if len(waveData) < len(noiseData):
        noiseData = noiseData[:audioLength]
    # 归一化
    waveData = waveData * 1.0 / (max(abs(waveData)))
    noiseData = noiseData * 1.0 / (max(abs(noiseData)))
    return waveData + noiseData
