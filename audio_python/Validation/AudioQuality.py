import librosa
import numpy
import pysepm
import seaborn
from matplotlib import pyplot as plt
from pesq import pesq
from pysepm import stoi

from Dataset.CommonVoice.CommonVoice import CommonVoice
from Dataset.DatasetList import get_dataset_instance
from Perturbation.AudioProcess import calculate_SNR
from Util.AudioUtil import pattern_to_name, pattern_types_dict, get_pattern_info_from_pattern_tag


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


def get_stoi(clean_audio, noise_audio):
    """
    计算语音的 STOI 值，范围[0,1]，值越大，可懂度越高.
    :param clean_audio: 原音频序列
    :param noise_audio: 现音频系列
    :return:
    """
    clean_sig, sr1 = librosa.load(clean_audio, sr=None)
    noise_sig, sr2 = librosa.load(noise_audio, sr=None)
    stoi_score = stoi(clean_sig, noise_sig, sr1, extended=False)
    return stoi_score


def get_NCM(clean_audio, noise_audio):
    """
    计算语音的 NCM 值
    :param clean_audio: 原音频序列
    :param noise_audio: 现音频系列
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
    cvd = CommonVoice("cv-corpus-chinese")
    noise_audios = cvd.get_noise_audio_clips_list()
    for noise_audio in noise_audios:
        audio, pattern_tag = cvd.get_name_and_pattern_tag(noise_audio)
        pattern, pattern_type = get_pattern_info_from_pattern_tag(pattern_tag)
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
    cvd = CommonVoice("cv-corpus-chinese")
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
    ncm_score = []
    x = []
    for i in range(0, len(clean_wavs)):
        pesq_score.append(get_pesq(cvd.clips_path + clean_wavs[i], cvd.noise_clips_path + noise_wavs[i]))
        stoi_score.append(get_stoi(cvd.clips_path + clean_wavs[i], cvd.noise_clips_path + noise_wavs[i]))
        ncm_score.append(get_NCM(cvd.clips_path + clean_wavs[i], cvd.noise_clips_path + noise_wavs[i]))
        x.append(i + 1)

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(x, pesq_score, label="PESQ")
    plt.plot(x, stoi_score, label="STOI")
    plt.plot(x, ncm_score, label="NCM")
    plt.legend()
    plt.xlabel("音频序号")
    plt.ylabel("分数")
    plt.show()


def draw_wer_chart():
    x = ["wav2vec2-\nlarge-960h", "s2t-large-\nlibrispeech-\nasr", "hubert-large-\nls960-ft",
         "data2vec-audio-\nbase-960h",
         "unispeech-\nlarge-1500h-\ncv-timit"]
    y1 = [0.09985528219971057, 0.10281855144373234, 0.06594996898904279, 0.08765763903245813, 0.23816415133347116]
    y2 = [0.23664806009234374, 0.2819929708497002, 0.15174695058920817, 0.26951967472951555, 0.4294673006684584]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(x, y1, label="原wer")
    plt.plot(x, y2, label="现wer")
    plt.legend()
    plt.ylabel("wer")
    plt.show()


def calculate_dataset_SNR(dataset):
    """
    计算数据集测试集SNR列表
    :param dataset:
    :return:
    """
    snr_list = []
    dataset_instance = get_dataset_instance(dataset)
    noise_test = dataset_instance.get_noise_testset_audio_clips_list()
    for noise_audio in noise_test:
        name, pattern_tag = dataset_instance.get_name_and_pattern_tag(noise_audio)
        if "sound_level" not in pattern_tag:
            snr = calculate_SNR(dataset_instance.clips_path + name, dataset_instance.noise_clips_path + noise_audio)
            snr_list.append(snr)
            print(noise_audio + "已计算")
    return snr_list


def SNR_statistic(snr_list):
    """
    求SNR统计量，有最大值、最小值、平均值、盒状图
    :param snr_list:
    :return:
    """
    seaborn.boxplot(data=snr_list)
    plt.show()
    return max(snr_list), min(snr_list), numpy.mean(snr_list)
