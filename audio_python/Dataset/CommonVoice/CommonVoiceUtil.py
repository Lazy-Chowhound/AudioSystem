import os

import numpy as np
import pydub


def write_noise_audio(path, noise_audio_name, noise_audio, sr, sample_width, channels):
    """
    将生成的扰动噪音以 wav 形式写入，然后转为 mp3 格式 然后删除原 wav
    :param path: 写入的地址
    :param noise_audio_name: 生成的音频文件名
    :param noise_audio: 音频数据
    :param sr: 采样率
    :param sample_width: 位深
    :param channels: 声道
    :return:
    """
    y = np.int16(noise_audio * 2 ** 15)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=int(sample_width), channels=int(channels))
    song.export(path + noise_audio_name, format="mp3", bitrate="64k")


def make_noise_audio_clips_dirs(path):
    """
    根据文件路径，生成所需文件夹
    :param path: D:/AudioSystem/NoiseAudio/cv-corpus-chinese/clips/xxx.mp3
    :return:
    """
    noise_audio_dir = path[0:path.rfind("/")]
    if not os.path.exists(noise_audio_dir):
        os.makedirs(noise_audio_dir)
