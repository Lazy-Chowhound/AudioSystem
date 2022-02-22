import json

from Dataset.CommonVoiceDataset.CommonVoiceDataset import CommonVoiceDataset
from Dataset.TimitDataset.TimitDataset import TimitDataset
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
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        audio = cvd.get_audio_clips_properties_by_page(page, page_size)
    elif dataset == "timit":
        td = TimitDataset("timit")
        audio = td.get_audio_clips_properties_by_page(page, page_size)
    return RpcResult.ok(json.dumps(audio, ensure_ascii=False))


@rpcApi
def get_waveform_graph(dataset, audio_name):
    """
    生成波形图
    :param dataset: cv-corpus-chinese
    :param audio_name: 音频名
    :return:
    """
    savingPath = None
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        savingPath = cvd.get_waveform_graph(audio_name)
    elif dataset == "timit":
        td = TimitDataset("timit")
        savingPath = td.get_waveform_graph(audio_name)
    return RpcResult.ok(savingPath)


@rpcApi
def get_mel_spectrum(dataset, audio_name):
    """
    生成 Mel频谱图
    :param dataset: cv-corpus-chinese
    :param audio_name: 音频名
    :return:
    """
    savingPath = None
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        savingPath = cvd.get_mel_spectrum(audio_name)
    elif dataset == "timit":
        td = TimitDataset("timit")
        savingPath = td.get_mel_spectrum(audio_name)
    return RpcResult.ok(savingPath)


@rpcApi
def remove_image(path):
    """
    删除图片
    :param path: 路径
    :return:
    """
    os.remove(path)
    return RpcResult.ok("Image removed")


if __name__ == '__main__':
    pass
