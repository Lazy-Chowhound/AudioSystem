import json
import math
import os
import random
from multiprocessing import Pool

from Dataset.DatasetList import get_dataset_instance
from Util.Annotation import rpcApi
from Util.AudioUtil import pattern_types_dict
from Util.RpcResult import RpcResult


@rpcApi
def get_num_of_clips_and_noise_clips(dataset):
    """
    获取原音频数量扰动音频的数量
    :param dataset: 数据集名称
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    return RpcResult.ok(json.dumps(dataset_instance.get_num_of_clips_and_noise_clips()))


@rpcApi
def get_audio_clips_pattern(dataset):
    """
    添加扰动时获取某数据集所有音频扰动情况
    :param dataset: 数据集名称
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    audio_set_pattern = dataset_instance.get_audio_clips_pattern()
    return RpcResult.ok(json.dumps(audio_set_pattern, ensure_ascii=False))


@rpcApi
def remove_current_noise_audio_clip(dataset, audio_name, pattern, pattern_type=None):
    """
    删除现有的扰动音频
    :param dataset: 数据集名称
    :param audio_name: 音频名称
    :param pattern: 扰动类别
    :param pattern_type: 具体扰动
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    dataset_instance.remove_current_noise_audio_clip(audio_name, pattern, pattern_type)
    return RpcResult.ok("")


@rpcApi
def add_gaussian_noise(dataset, audio_name):
    """
    添加高斯白噪声
    :param dataset: 数据集名称
    :param audio_name: 音频名称
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    dataset_instance.add_gaussian_noise(audio_name)
    return RpcResult.ok("")


@rpcApi
def add_sound_level(dataset, audio_name, pattern_type):
    """
    添加 sound level 扰动
    :param dataset: 数据集名称
    :param audio_name: 音频名称
    :param pattern_type: 具体扰动
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    dataset_instance.add_sound_level(audio_name, pattern_type)
    return RpcResult.ok("")


@rpcApi
def add_natural_sounds(dataset, audio_name, pattern_type):
    """
    添加 natural sound 扰动
    :param dataset: 数据集名称
    :param audio_name: 音频名称
    :param pattern_type: 具体扰动
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    dataset_instance.add_natural_sounds(audio_name, pattern_type)
    return RpcResult.ok("")


@rpcApi
def add_animal(dataset, audio_name, pattern_type):
    """
    添加 animal 扰动
    :param dataset: 数据集名称
    :param audio_name: 音频名称
    :param pattern_type: 具体扰动
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    dataset_instance.add_animal(audio_name, pattern_type)
    return RpcResult.ok("")


@rpcApi
def add_sound_of_things(dataset, audio_name, pattern_type):
    """
    添加 sound of things 扰动
    :param dataset: 数据集名称
    :param audio_name: 音频名称
    :param pattern_type: 具体扰动
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    dataset_instance.add_sound_of_things(audio_name, pattern_type)
    return RpcResult.ok("")


@rpcApi
def add_human_sounds(dataset, audio_name, pattern_type):
    """
    添加 human sounds 扰动
    :param dataset: 数据集名称
    :param audio_name: 音频名称
    :param pattern_type: 具体扰动
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    dataset_instance.add_human_sounds(audio_name, pattern_type)
    return RpcResult.ok("")


@rpcApi
def add_music(dataset, audio_name, pattern_type):
    """
    添加 music 扰动
    :param dataset: 数据集名称
    :param audio_name: 音频名称
    :param pattern_type: 具体扰动
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    dataset_instance.add_music(audio_name, pattern_type)
    return RpcResult.ok("")


@rpcApi
def add_source_ambiguous_sounds(dataset, audio_name, pattern_type):
    """
    添加 source_ambiguous_sounds 扰动
    :param dataset: 数据集名称
    :param audio_name: 音频名称
    :param pattern_type: 具体扰动
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    dataset_instance.add_source_ambiguous_sounds(audio_name, pattern_type)
    return RpcResult.ok("")


@rpcApi
def add_randomly_multiProcess(dataset, process_num, set_type="all", given_list=None):
    """
    数据集全部音频多线程添加扰动
    :param process_num: 进程数
    :param dataset: 数据集名称
    :param set_type: test/dev/train/all
    :param given_list: 给定音频列表
    :return:
    """
    dataset_instance = get_dataset_instance(dataset)
    audio_list = []
    if set_type == "all":
        audio_list = dataset_instance.get_audio_clips_list()
    elif set_type == "test":
        audio_list = dataset_instance.get_testset_audio_clips_list()
    elif set_type == "train":
        audio_list = dataset_instance.get_trainset_audio_clips_list()
    elif set_type == "certain":
        audio_list = given_list
    task_slice = math.ceil(len(audio_list) / process_num)
    pool = Pool(process_num)
    for i in range(0, process_num):
        pool.apply_async(add_pattern_range,
                         args=(dataset, audio_list, i * task_slice, min((i + 1) * task_slice, len(audio_list)),))
    pool.close()
    pool.join()


def add_pattern_range(dataset, audio_list, start, end):
    """
    范围添加扰动
    :param dataset: 数据集名称
    :param audio_list: 音频列表
    :param start: 第几个开始
    :param end: 第几个结束
    :return:
    """
    print('process %s working...' % (os.getpid()))
    for audio in audio_list[start:end]:
        add_pattern_randomly(dataset, audio)


def add_pattern_randomly(dataset, file):
    """
    随机加噪声
    :param dataset: 数据集名称
    :param file: 音频名称
    :return:
    """
    try:
        p = random.randint(3, 8)
        if p == 1:
            add_gaussian_noise(dataset, file)
        elif p == 2:
            ptype = pattern_types_dict["Sound level"]
            add_sound_level(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 3:
            ptype = pattern_types_dict["Animal"]
            add_animal(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 4:
            ptype = pattern_types_dict["Sound of things"]
            add_sound_of_things(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 5:
            ptype = pattern_types_dict["Human sounds"]
            add_human_sounds(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 6:
            ptype = pattern_types_dict["Natural sounds"]
            add_natural_sounds(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 7:
            ptype = pattern_types_dict["Music"]
            add_music(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 8:
            ptype = pattern_types_dict["Source-ambiguous sounds"]
            add_source_ambiguous_sounds(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        print(file + "已加噪")
    except Exception as e:
        print(dataset + ":" + file + " fail ", e)
