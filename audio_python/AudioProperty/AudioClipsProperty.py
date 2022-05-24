import json
import os

from Dataset.DatasetList import get_dataset_instance
from Util.Annotation import rpcApi
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
    dataset_instance = get_dataset_instance(dataset)
    audio = dataset_instance.get_audio_clips_properties_by_page(page, page_size)
    return RpcResult.ok(json.dumps(audio, ensure_ascii=False))


@rpcApi
def get_waveform_graph(dataset, audio_name):
    """
    生成波形图
    :param dataset: cv-corpus-chinese
    :param audio_name: 音频名
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    savingPath = dataset_instance.get_waveform_graph(dataset_instance.clips_path + audio_name, audio_name)
    return RpcResult.ok(savingPath)


@rpcApi
def get_mel_spectrum(dataset, audio_name):
    """
    生成 Mel频谱图
    :param dataset: cv-corpus-chinese
    :param audio_name: 音频名
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    savingPath = dataset_instance.get_mel_spectrum(dataset_instance.clips_path + audio_name, audio_name)
    return RpcResult.ok(savingPath)


@rpcApi
def get_contrast_graph(dataset, audio_name):
    """
    获取扰动前后对比属性图
    :param dataset:
    :param audio_name:
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    noise_audio_name = dataset_instance.get_noise_clip_name(audio_name)
    before_waveform = dataset_instance.get_waveform_graph(dataset_instance.clips_path + audio_name, audio_name)
    after_waveform = dataset_instance.get_waveform_graph(dataset_instance.noise_clips_path + noise_audio_name,
                                                         noise_audio_name)
    before_mel = dataset_instance.get_mel_spectrum(dataset_instance.clips_path + audio_name, audio_name)
    after_mel = dataset_instance.get_mel_spectrum(dataset_instance.noise_clips_path + noise_audio_name,
                                                  noise_audio_name)
    return RpcResult.ok(json.dumps([before_waveform, after_waveform, before_mel, after_mel]))


@rpcApi
def remove_image(path):
    """
    删除图片
    :param path: 路径
    :return:
    """
    os.remove(path)
    return RpcResult.ok("Image removed")
