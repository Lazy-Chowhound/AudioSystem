import json

import librosa
import pymysql
from matplotlib import pyplot as plt
from pesq import pesq
from pystoi import stoi
import pysepm
from Dataset.CommonVoiceDataset.CommonVoiceDataset import CommonVoiceDataset
from Dataset.DatasetList import get_dataset_instance
from Util.Annotation import rpcApi
from Util.AudioUtil import pattern_to_name, pattern_types_dict, get_pattern_info_from_name
from Util.RpcResult import RpcResult


@rpcApi
def get_models(user_name):
    """
    获取用户上传模型
    :return:
    """
    model_list = []
    connect = pymysql.Connect(host="localhost", port=3306, user="root",
                              passwd="061210", db="audioset", charset="utf8")
    cursor = connect.cursor()
    cursor.execute(
        "select name from modelhistory where user = '%s'" % (user_name,))
    for item in cursor.fetchall():
        model_list.append(item[0])
    cursor.close()
    connect.close()
    return RpcResult.ok(json.dumps(model_list, ensure_ascii=False))


@rpcApi
def get_validation_results_by_page(dataset, model_name, page, page_size):
    """
    获取验证内容
    :param dataset:
    :param model_name:
    :param page:
    :param page_size:
    :return:
    """
    try:
        dataset_instance = get_dataset_instance(dataset)
        dataset_instance.load_model(model_name)
        results = dataset_instance.get_validation_results_by_page(page, page_size)
        return RpcResult.ok(json.dumps(results, ensure_ascii=False))
    except Exception as e:
        return RpcResult.error(e)


def get_pesq(clean_audio, noise_audio):
    """
    计算两个音频的 pesq,范围[-0.5,4.5]，越高越好
    :param clean_audio: 原始文件
    :param noise_audio: 待评估文件
    :return: score
    """
    clean_sig, sr1 = librosa.load(clean_audio, sr=16000)
    noise_sig, sr2 = librosa.load(noise_audio, sr=16000)
    pseq_score = pesq(sr1, clean_sig, noise_sig, 'wb')
    return pseq_score


def get_WSS(clean_audio, noise_audio):
    """
    计算语音的 WSS 值，值越小越好
    :param clean_audio:
    :param noise_audio:
    :return:
    """
    clean_sig, sr1 = librosa.load(clean_audio, sr=None)
    noise_sig, sr2 = librosa.load(noise_audio, sr=None)
    wss_score = pysepm.wss(clean_sig, noise_sig, sr1)
    return wss_score


def get_stoi(clean_audio, noise_audio):
    """
    计算语音的 STOI 值，范围[0,1]，值越大，可懂度越高.
    :param clean_audio:
    :param noise_audio:
    :return:
    """
    clean_sig, sr1 = librosa.load(clean_audio, sr=None)
    noise_sig, sr2 = librosa.load(noise_audio, sr=None)
    stoi_score = stoi(clean_sig, noise_sig, sr1, extended=False)
    return stoi_score


def get_NCM(clean_audio, noise_audio):
    """
    计算语音的 NCM 值
    :param clean_audio:
    :param noise_audio:
    :return:
    """
    clean_sig, sr1 = librosa.load(clean_audio, sr=16000)
    noise_sig, sr2 = librosa.load(noise_audio, sr=16000)
    ncm_score = pysepm.ncm(clean_sig, noise_sig, sr1)
    return ncm_score


def get_pattern_types_dict():
    """
    返回 common voice 扰动的列表
    :return: {"Gaussian noise":[[原音频,扰动音频],[]...]},
              "Sound level":{"Louder":[[],[]...],
                             "Quieter":[[],[]...],
                             ...
                             }
              ...
              }
    """
    p_t_dict = {}
    for item in pattern_to_name.keys():
        if item == "Gaussian noise":
            p_t_dict[item] = []
        else:
            p_t_dict[item] = {}
            for sub_item in pattern_types_dict.get(item):
                p_t_dict[item][sub_item] = []
    cvd = CommonVoiceDataset("cv-corpus-chinese")
    noise_audios = cvd.get_noise_audio_clips_list()
    for noise_audio in noise_audios:
        audio, pattern_tag = cvd.get_name_and_pattern_tag(noise_audio)
        pattern, pattern_type = get_pattern_info_from_name(pattern_tag)
        if pattern == "Gaussian noise":
            p_t_dict[pattern].append([audio, noise_audio])
        else:
            p_t_dict[pattern][pattern_type].append([audio, noise_audio])
    return p_t_dict


def draw_quality_and_intelligibility_chart():
    """
    common voice 音频质量和可懂度图
    :return:
    """
    p_t_dict = get_pattern_types_dict()
    clean_wavs = []
    noise_wavs = []
    for item in p_t_dict.keys():
        if type(p_t_dict.get(item)).__name__ == 'list':
            clean_wavs.append(p_t_dict[item][0][0])
            noise_wavs.append(p_t_dict[item][0][1])
        else:
            for sub_item in p_t_dict.get(item).keys():
                if sub_item != "Speed" and len(p_t_dict[item][sub_item]) != 0:
                    clean_wavs.append(p_t_dict[item][sub_item][0][0])
                    noise_wavs.append(p_t_dict[item][sub_item][0][1])
    pesq_score = []
    stoi_score = []
    wss_score = []
    ncm_score = []
    x = []
    for i in range(0, len(clean_wavs)):
        pesq_score.append(get_pesq(clean_wavs[i], noise_wavs[i]))
        stoi_score.append(get_stoi(clean_wavs[i], noise_wavs[i]))
        wss_score.append(get_WSS(clean_wavs[i], noise_wavs[i]))
        ncm_score.append(get_NCM(clean_wavs[i], noise_wavs[i]))
        x.append(i + 1)

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(x, pesq_score, label="PESQ")
    plt.plot(x, stoi_score, label="STOI")
    plt.plot(x, ncm_score, label="NCM")
    plt.legend()
    plt.xlabel("音频序号")
    plt.ylabel("分数")
    plt.show()
