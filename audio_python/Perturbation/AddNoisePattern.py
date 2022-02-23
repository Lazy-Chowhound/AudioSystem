import json
import logging
from multiprocessing import Pool

from Dataset.CommonVoiceDataset.CommonVoiceDataset import CommonVoiceDataset
from Dataset.TimitDataset.TimitDataset import TimitDataset
from Perturbation.AudioProcess import *
from Util.Annotation import rpcApi
from Util.AudioUtil import *
from Util.RpcResult import RpcResult


@rpcApi
def get_audio_clips_pattern(dataset):
    """
    添加扰动时获取某数据集所有音频扰动情况
    :param dataset: cv-corpus-chinese or timit
    :return:
    """
    audio_set_pattern = []
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        audio_set_pattern = cvd.get_audio_clips_pattern()
    elif dataset == "timit":
        td = TimitDataset("timit")
        audio_set_pattern = td.get_audio_clips_pattern()
    return RpcResult.ok(json.dumps(audio_set_pattern, ensure_ascii=False))


@rpcApi
def remove_current_noise_audio_clip(dataset, audio_name, pattern, pattern_type=None):
    """
    删除现有的扰动音频
    :param dataset: cv-corpus-chinese or timit
    :param audio_name: common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :param pattern: Animal
    :param pattern_type: Wild animals
    :return:
    """
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        cvd.remove_current_noise_audio_clip(audio_name, pattern, pattern_type)
    elif dataset == "timit":
        td = TimitDataset("timit")
        td.remove_current_noise_audio_clip(audio_name, pattern, pattern_type)
    return RpcResult.ok("")


@rpcApi
def add_gaussian_noise(dataset, audio_name):
    """
    添加高斯白噪声
    :param dataset: cv-corpus-chinese or timit
    :param audio_name: common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :return:
    """
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        cvd.add_gaussian_noise(audio_name)
    elif dataset == "timit":
        td = CommonVoiceDataset("timit")
        td.add_gaussian_noise(audio_name)
    return RpcResult.ok("")


@rpcApi
def add_sound_level(dataset, audio_name, pattern_type):
    """
    添加 sound level 扰动
    :param dataset: cv-corpus-chinese or timit
    :param audio_name: common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :param pattern_type: 具体扰动 {louder:更响,quieter:更静,pitch:英高,speed:变速（更快）}
    :return:
    """
    result = ""
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        result = cvd.add_sound_level(audio_name, pattern_type)
    elif dataset == "timit":
        td = CommonVoiceDataset("timit")
        td.add_sound_level(audio_name, pattern_type)
    return RpcResult.ok(result)


@rpcApi
def add_natural_sounds(dataset, audio_name, pattern_type):
    """
    添加 natural sound 扰动
    :param dataset: cv-corpus-chinese or timit
    :param audio_name: common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :param pattern_type:
    :return:
    """
    result = ""
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        result = cvd.add_natural_sounds(audio_name, pattern_type)
    elif dataset == "timit":
        td = CommonVoiceDataset("timit")
        td.add_natural_sounds(audio_name, pattern_type)
    return RpcResult.ok(result)


@rpcApi
def add_animal(dataset, audio_name, pattern_type):
    """
    添加 animal 扰动
    :param dataset: cv-corpus-chinese or timit
    :param audio_name: common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :param pattern_type:
    :return:
    """
    result = ""
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        result = cvd.add_animal(audio_name, pattern_type)
    elif dataset == "timit":
        td = CommonVoiceDataset("timit")
        td.add_animal(audio_name, pattern_type)
    return RpcResult.ok(result)


@rpcApi
def add_sound_of_things(dataset, audio_name, pattern_type):
    """
    添加 sound of things 扰动
    :param dataset: cv-corpus-chinese or timit
    :param audio_name: common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :param pattern_type:
    :return:
    """
    result = ""
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        result = cvd.add_sound_of_things(audio_name, pattern_type)
    elif dataset == "timit":
        td = CommonVoiceDataset("timit")
        td.add_sound_of_things(audio_name, pattern_type)
    return RpcResult.ok(result)


@rpcApi
def add_human_sounds(dataset, audio_name, pattern_type):
    """
    添加 human sounds 扰动
    :param dataset: cv-corpus-chinese or timit
    :param audio_name: 形如 common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :param pattern_type:
    :return:
    """
    result = ""
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        result = cvd.add_human_sounds(audio_name, pattern_type)
    elif dataset == "timit":
        td = CommonVoiceDataset("timit")
        td.add_human_sounds(audio_name, pattern_type)
    return RpcResult.ok(result)


@rpcApi
def add_music(dataset, audio_name, pattern_type):
    """
    添加 music 扰动
    :param dataset: cv-corpus-chinese or timit
    :param audio_name: 形如 common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :param pattern_type:
    :return:
    """
    result = ""
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        result = cvd.add_music(audio_name, pattern_type)
    elif dataset == "timit":
        td = CommonVoiceDataset("timit")
        td.add_music(audio_name, pattern_type)
    return RpcResult.ok(result)


@rpcApi
def add_source_ambiguous_sounds(dataset, audio_name, pattern_type):
    """
    添加 source_ambiguous_sounds 扰动
    :param dataset: cv-corpus-chinese or timit
    :param audio_name: common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :param pattern_type:
    :return:
    """
    result = ""
    if dataset == "cv-corpus-chinese":
        cvd = CommonVoiceDataset("cv-corpus-chinese")
        result = cvd.add_source_ambiguous_sounds(audio_name, pattern_type)
    elif dataset == "timit":
        td = CommonVoiceDataset("timit")
        td.add_source_ambiguous_sounds(audio_name, pattern_type)
    return RpcResult.ok(result)


def add_randomly_multiProcess(dataset, process_num):
    """
    多线程添加扰动
    :param process_num: 进程数
    :param dataset: cv-corpus-chinese or timit
    :return:
    """

    audio_list = []
    if dataset == "cv-corpus-chinese":
        audio_list = CommonVoiceDataset("cv-corpus-chinese").get_audio_clips_list()
    elif dataset == "timit":
        audio_list = TimitDataset("timit").get_audio_clips_list()
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
    :param dataset:
    :param audio_list:
    :param start:
    :param end:
    :return:
    """
    print('process %s working...' % (os.getpid()))
    for audio in audio_list[start:end]:
        add_pattern_randomly(dataset, audio)


def add_pattern_randomly(dataset, file):
    """
    随机加噪声
    :param dataset: cv-corpus-chinese or timit
    :param file: common_voice_zh-CN_18524189.mp3 or DR1/FCJF0/SA1_n.wav
    :return:
    """
    try:
        p = random.randint(1, 8)
        if p == 1:
            add_gaussian_noise(dataset, file)
        elif p == 2:
            ptype = sound_level_pattern_types
            add_sound_level(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 3:
            ptype = animal_pattern_types
            add_animal(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 4:
            ptype = sound_of_things_pattern_types
            add_sound_of_things(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 5:
            ptype = human_sounds_pattern_types
            add_human_sounds(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 6:
            ptype = natural_sounds_pattern_types
            add_natural_sounds(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 7:
            ptype = music_pattern_types
            add_music(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 8:
            ptype = source_ambiguous_sounds_pattern_types
            add_source_ambiguous_sounds(dataset, file, ptype[random.randint(0, len(ptype) - 1)])
    except Exception as e:
        logging.warning(dataset + ":" + file + " fail ", e)


if __name__ == '__main__':
    pass
