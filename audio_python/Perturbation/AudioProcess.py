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
    # 信号功率
    P_signal = np.sum(abs(wave_data) ** 2) / len(wave_data)
    # 噪声功率
    P_noise = P_signal / 10 ** (snr / 10.0)
    noise = np.random.normal(0, 1, size=len(wave_data))
    noise = normalize(noise)
    return noise * np.sqrt(P_noise).astype(data_type)


def volume_augment(wave_data, min_gain_dB, max_gain_dB):
    """
    改变音量
    :param wave_data: numpy数组
    :param min_gain_dB:
    :param max_gain_dB:
    :return:
    """
    data_type = wave_data[0].dtype
    gain = random.uniform(min_gain_dB, max_gain_dB)
    gain = 10. ** (gain / 20.)
    wave_data = wave_data * gain
    wave_data = wave_data.astype(data_type)
    return wave_data


def louder(wave_data):
    """
    提高响度
    :param wave_data: numpy数组
    :return:
    """
    return volume_augment(wave_data, 0, 10)


def quieter(wave_data):
    """
    降低响度
    :param wave_data: numpy数组
    :return:
    """
    return volume_augment(wave_data, -10, 0)


def change_pitch(wave_data, sr):
    """
    改变音高
    :param wave_data:
    :param sr:
    :return:
    """
    pitch_list = list(range(-5, 6))
    pitch_list.remove(0)
    pitch = random.choice(pitch_list)
    noise_audio = librosa.effects.pitch_shift(wave_data, sr, n_steps=float(pitch))
    return noise_audio


def change_speed(wave_data):
    speed = random.uniform(0.9, 1.1)
    noise_data = librosa.effects.time_stretch(wave_data, speed)
    return noise_data


def add_noise(wave_data, noise_data, amplitude=0.3):
    """
    音频添加噪声噪声
    :param wave_data: 原始音频 ndarray
    :param noise_data: 噪声音频 ndarray
    :param amplitude: 振幅缩放比
    :return:
    """
    noise_data = align_audio_length(wave_data, noise_data)
    wave_data = wave_data * 1.0 / (max(abs(wave_data)))
    noise_data = noise_data * amplitude / (max(abs(noise_data)))
    return wave_data + noise_data


def add_noise_certain_snr(wave_data, noise_data, min_snr, max_snr):
    """
    指定信噪比内添加噪声
    :param wave_data: 原始音频 ndarray
    :param noise_data: 噪声音频 ndarray
    :param min_snr: 最低信噪比
    :param max_snr: 最高信噪比
    :return:
    """
    noise_data = align_audio_length(wave_data, noise_data)
    snr = random.randint(min_snr, max_snr)
    # 信号功率
    P_signal = np.sum(abs(wave_data) ** 2) / len(wave_data)
    # 指定信噪比下的噪声功率
    P_noise = P_signal / (10 ** (snr / 10))
    # 目前的噪声功率
    cur_P_noise = np.sum(abs(noise_data) ** 2) / len(noise_data)
    # 计算得出缩放噪声数据使得信噪比为指定数值
    noise_data = noise_data * math.sqrt(P_noise / cur_P_noise)
    return wave_data + noise_data


def align_audio_length(wave_data, noise_data):
    """
    使噪声数据和音频数据长度一致
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
    return noise_data


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
