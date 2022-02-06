import json

import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Util.Annotation import rpcApi
from Util.AudioUtil import *
from Util.RpcResult import RpcResult


@rpcApi
def get_audio_clips_properties_by_page(dataset, page, page_size):
    """
    分页获取音频及其属性
    :param dataset: cv-corpus-chinese
    :param page: 页数
    :param page_size: 页面大小
    :return:
    """
    audio = []
    audio_list = get_audio_clips_list(dataset)
    audio.append({'total': len(audio_list)})
    for i in range((int(page) - 1) * int(page_size),
                   min(int(page) * int(page_size), len(audio_list))):
        audio_property = get_audio_clip_properties(dataset, audio_list[i])
        audio_property['key'] = i + 1
        audio.append(audio_property)
    return RpcResult.ok(json.dumps(audio, ensure_ascii=False))


def get_audio_clip_properties(dataset, audio_name):
    """
    获取某条音频所有属性
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :return:
    """
    audio = get_audio_clips_path(dataset) + audio_name
    audio_property = {}
    detail = get_audio_clip_detail(dataset, audio_name)
    audio_property['name'] = audio_name
    audio_property['size'] = str(get_duration(audio)) + "秒"
    audio_property['channel'] = "单" if get_channels(audio) == 1 else "双"
    audio_property['sampleRate'] = str(getSamplingRate(audio)) + "Hz"
    audio_property['bitDepth'] = str(get_bit_depth(audio)) + "bit"
    audio_property['content'] = detail['sentence']
    return audio_property


def get_audio_clips_list(dataset):
    """
    获取目录下所有音频文件名
    :param dataset: cv-corpus-arabic
    :return:
    """
    path = get_audio_clips_path(dataset)
    audioList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp3':
                audioList.append(file)
    return audioList


def get_audio_clip_detail(dataset, audio_name):
    """
    获取指定音频的详情
    :param dataset: cv-corpus-chinese
    :param audio_name:
    :return:
    """
    path = get_audio_set_path(dataset)
    files = ['validated.tsv', 'invalidated.tsv', 'other.tsv']
    detail = {}
    for file in files:
        train = pd.read_csv(os.path.join(path, file), sep='\t', header=0)
        for index, row in train.iterrows():
            if audio_name in row['path']:
                detail['id'] = index
                for item in row.items():
                    detail[item[0]] = item[1]
                break
    return detail


@rpcApi
def get_waveform_graph(dataset, audio_name):
    """
    生成波形图
    :param dataset: cv-corpus-chinese
    :param audio_name: 音频名
    :return:
    """
    audio = os.path.join(get_audio_clips_path(dataset), audio_name)
    sig, sr = librosa.load(audio, sr=None)
    plt.figure(figsize=(8, 5))
    librosa.display.waveshow(sig, sr=sr)
    plt.ylabel('Amplitude')
    savingPath = "D:/AudioSystem/WaveImage/" + audio_name + ".jpg"
    plt.savefig(savingPath)
    return RpcResult.ok(savingPath)


@rpcApi
def get_mel_spectrum(dataset, audio_name):
    """
    生成 Mel频谱图
    :param dataset: cv-corpus-chinese
    :param audio_name: 音频名
    :return:
    """
    audio = os.path.join(get_audio_clips_path(dataset), audio_name)
    sig, sr = librosa.load(audio, sr=None)
    S = librosa.feature.melspectrogram(y=sig, sr=sr)
    plt.figure(figsize=(8, 5))
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
                             y_axis='mel', fmax=8000, x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    savingPath = "D:/AudioSystem/SpectrumImage/" + audio_name + ".jpg"
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


def get_duration(audio):
    """
    获取音频时长
    :param audio: 音频路径
    :return:
    """
    sig, sr = librosa.load(audio, sr=None)
    return round(librosa.get_duration(sig, sr), 2)


def get_channels(audio):
    """
    获取声道
    :param audio: 音频路径
    :return:
    """
    song = AudioSegment.from_mp3(audio)
    return song.channels


def get_bit_depth(audio):
    """
    获取位深
    :param audio: 音频路径
    :return:
    """
    song = AudioSegment.from_mp3(audio)
    return song.sample_width * 8


@rpcApi
def remove_image(path):
    """
    删除图片
    :param path: 路径
    :return:
    """
    os.remove(path)
    return RpcResult.ok("Image removed")
