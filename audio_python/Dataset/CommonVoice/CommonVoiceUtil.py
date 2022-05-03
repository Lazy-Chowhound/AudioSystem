import os

import soundfile
from pydub import AudioSegment


def write_noise_audio(path, noise_audio_name, noiseAudio, sr):
    """
    将生成的扰动噪音以 wav 形式写入，然后转为 mp3 格式 然后删除原 wav
    :param path: 写入的地址
    :param noise_audio_name: 生成的音频文件名
    :param noiseAudio: 音频数据
    :param sr: 采样率
    :return:
    """
    soundfile.write(path + noise_audio_name, noiseAudio, sr)
    transform_wav_to_mp3(path, noise_audio_name)
    os.remove(path + noise_audio_name)


def transform_wav_to_mp3(path, audio_name):
    """
    wav转 mp3
    :param path: D:/AudioSystem/noiseAudio/cv-corpus-chinese/clips/
    :param audio_name: common_voice_zh-CN_18524189_gaussian_white_noise.wav
    :return: 生成的 wav 地址
    """
    audio = AudioSegment.from_wav(path + audio_name)
    audio_name = audio_name.replace(".wav", ".mp3")
    audio.export(path + audio_name, format="mp3")
    return path, audio_name


def make_noise_audio_clips_dirs(path):
    """
    根据文件路径，生成所需文件夹
    :param path: D:/AudioSystem/NoiseAudio/cv-corpus-chinese/clips/xxx.mp3
    :return:
    """
    noise_audio_dir = path[0:path.rfind("/")]
    if not os.path.exists(noise_audio_dir):
        os.makedirs(noise_audio_dir)