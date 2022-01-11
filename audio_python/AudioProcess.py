import random

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
    print("pitch:" + str(pitch))
    noiseAudio = librosa.effects.pitch_shift(wavData, sr, n_steps=float(pitch))
    return noiseAudio


def addNoisePattern(path, audioName, pattern):
    wavePath, waveName = trans_mp3_to_wav(path, audioName)
    sig, sr = librosa.load(wavePath + waveName, sr=None)

    noiseAudio = sig
    noiseWaveName = None
    if pattern == "gaussian_white_noise":
        noiseAudio = gaussian_white_noise(sig, snr=5)
        noiseWaveName = addTag(waveName, "gaussian_white_noise")
    elif pattern == "louder":
        noiseAudio = louder(sig)
        noiseWaveName = addTag(waveName, "sound_level_louder")
    elif pattern == "quieter":
        noiseAudio = quieter(sig)
        noiseWaveName = addTag(waveName, "sound_level_quieter")
    elif pattern == "pitch":
        noiseAudio = changePitch(sig, sr)
        noiseWaveName = addTag(waveName, "sound_level_pitch")
    elif pattern == "speed":
        sr = sr * 2
        noiseWaveName = addTag(waveName, "sound_level_speed")
    soundfile.write(wavePath + noiseWaveName, noiseAudio, sr)
    trans_wav_to_mp3(wavePath, noiseWaveName)
    removeAudio(wavePath, waveName)
    removeAudio(wavePath, noiseWaveName)


if __name__ == '__main__':
    addNoisePattern("D:/AudioSystem/Audio/cv-corpus-chinese/clips/",
                    "common_voice_zh-CN_18524189.mp3", "speed")
