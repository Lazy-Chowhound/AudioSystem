import math
import random

import librosa
import numpy as np


def normalize(wave_data):
    """
    将标准正态分布样本变更加标准化
    :param wave_data: ndarray
    :return:
    """
    standardDeviation = np.std(wave_data)
    return (wave_data - np.mean(wave_data)) / standardDeviation


def gaussian_white_noise(wave_data, snr):
    """
    高斯白噪声
    :param wave_data: numpy数组
    :param snr:
    :return:
    """
    data_type = wave_data[0].dtype
    P_signal = np.sum(abs(wave_data) ** 2) / len(wave_data)  # 信号功率
    P_noise = P_signal / 10 ** (snr / 10.0)  # 噪声功率
    noise = np.random.normal(0, 1, size=len(wave_data))
    noise = normalize(noise)
    return noise * np.sqrt(P_noise).astype(data_type)


def louder(wave_data):
    """
    提高响度
    :param wave_data: numpy数组
    :return:
    """
    return wave_data * 5


def quieter(wave_data):
    """
    降低响度
    :param wave_data: numpy数组
    :return:
    """
    return wave_data / 5


def change_pitch(wave_data, sr):
    """
    改变音高
    :param wave_data:
    :param sr:
    :return:
    """
    pitch = random.randint(5, 10) * random.randrange(-1, 2, 2)
    noise_audio = librosa.effects.pitch_shift(wave_data, sr, n_steps=float(pitch))
    return noise_audio


def add_noise(wave_data, noise_data):
    """
    音频添加噪声噪声
    :param wave_data: 原始音频 ndarray
    :param noise_data: 噪声音频 ndarray
    :return:
    """
    audio_length = len(wave_data)
    # 先使噪声长度大于等于音频，然后再截取成一样
    if len(wave_data) > len(noise_data):
        noise_data = np.tile(noise_data, math.ceil(len(wave_data) / len(noise_data)))
    if len(wave_data) < len(noise_data):
        noise_data = noise_data[:audio_length]
    # 归一化
    wave_data = wave_data * 1.0 / (max(abs(wave_data)))
    noise_data = noise_data * 0.3 / (max(abs(noise_data)))
    return wave_data + noise_data


def calculate_SNR(clean_file, original_file):
    """
    计算信噪比
    :param clean_file: 干净语音
    :param original_file: 含噪声语音
    :return:
    """
    clean_sig, clean_sr = librosa.load(clean_file, sr=None)
    original_sig, ori_sr = librosa.load(original_file, sr=None)
    noise_sig = original_sig - clean_sig
    SNR = 10 * np.log10((np.sum(clean_sig ** 2)) / (np.sum(noise_sig ** 2)))
    return SNR
