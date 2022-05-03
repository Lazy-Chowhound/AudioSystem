import re

import librosa
import soundfile

# 项目路径
PROJECT_PATH = "D:/AudioSystem/"
# 数据集路径
AUDIO_SETS_PATH = PROJECT_PATH + "Audio/"
# 添加完扰动的音频数据集路径
NOISE_AUDIO_SETS_PATH = PROJECT_PATH + "NoiseAudio/"
# 噪声文件路径
SOURCE_NOISES_PATH = PROJECT_PATH + "Noise/"
# 波形图路径
WAVEFORM_GRAPH_PATH = PROJECT_PATH + "WaveImage/"
# Mel频谱图路径
MEL_SPECTRUM_PATH = PROJECT_PATH + "SpectrumImage/"
# ASR模型路径
MODEL_PATH = PROJECT_PATH + "Models/"

pattern_to_name = {"Gaussian noise": "gaussian_white_noise",
                   "Sound level": "sound_level",
                   "Animal": "animal",
                   "Source-ambiguous sounds": "source_ambiguous_sounds",
                   "Natural sounds": "natural_sounds",
                   "Sound of things": "sound_of_things",
                   "Human sounds": "human_sounds",
                   "Music": "music"}

name_to_pattern = {"gaussian_white_noise": "Gaussian noise",
                   "sound_level": "Sound level",
                   "animal": "Animal",
                   "source_ambiguous_sounds": "Source-ambiguous sounds",
                   "natural_sounds": "Natural sounds",
                   "sound_of_things": "Sound of things",
                   "human_sounds": "Human sounds",
                   "music": "Music"}

pattern_types_dict = {
    "Sound level": ["Louder", "Quieter", "Pitch", "Speed"],
    "Animal": ["Pets", "Livestock", "Wild animals"],
    "Source-ambiguous sounds": ["Generic impact sounds", "Surface contact", "Deformable shell",
                                "Onomatopoeia", "Other sourceless"],
    "Natural sounds": ["Wind", "Thunderstorm", "Water", "Fire"],
    "Sound of things": ["Vehicle", "Engine", "Domestic sounds", "Bell", "Alarm", "Mechanisms", "Tools",
                        "Explosion", "Wood", "Glass", "Liquid", "Miscellaneous sources",
                        "Specific impact sounds"],
    "Human sounds": ["Human voice", "Whistling", "Respiratory sounds", "Human locomotion", "Hands",
                     "Heartbeat", "Human group actions", "Digestive", "Otoacoustic emission"],
    "Music": ["Musical instrument", "Music genre", "Musical concepts", "Music role", "Music mood"]
}


def add_tag(name, tag):
    """
    给添加扰动后生成的文件名打上对应扰动的类型
    :param name: common_voice_zh-CN_18524189.mp3
    :param tag: sound_level
    :return: common_voice_zh-CN_18524189_sound_level.mp3
    """
    pos = name.index(".")
    return name[0:pos] + "_" + tag + name[pos:]


def suffix_to_pattern_type(suffix):
    """
    将音频名称扰动后缀转换为对应的扰动类型
    :param suffix: gaussian_white_noise
    :return: Gaussian white noise
    """
    return suffix.replace("_", " ").capitalize()


def pattern_type_to_suffix(pattern_type):
    """
    扰动类型转换为对应后缀
    :param pattern_type: Gaussian white noise
    :return: gaussian_white_noise
    """
    return pattern_type.replace(" ", "_").lower()


def get_pattern_info_from_pattern_tag(pattern_tag):
    """
    从名称后缀解析出扰动类别和具体类型
    :param pattern_tag: animal_wild_animals
    :return: animal,wild animals
    """
    if "gaussian_white_noise" in pattern_tag:
        return name_to_pattern["gaussian_white_noise"], suffix_to_pattern_type("gaussian_white_noise")
    else:
        for key, value in name_to_pattern.items():
            if key in pattern_tag:
                return name_to_pattern[key], suffix_to_pattern_type(pattern_tag.replace(key + "_", "", 1))


def get_source_noises_path(pattern, pattern_type):
    return SOURCE_NOISES_PATH + pattern + "/" + pattern_type + ".wav"


def cut_audio(path, start, end=None):
    """
    截取音频
    :param path:
    :param start: 开始的秒数
    :param end: 结束的秒数，默认最后
    :return:
    """
    sig, sr = librosa.load(path, sr=None)
    if end is None:
        audio_dst = sig[start * sr:]
    else:
        audio_dst = sig[start * sr:end * sr]
    soundfile.write(path[0: path.find(".")] + "_cut" + ".wav", audio_dst, sr)


def get_error_audio_clips(source_file_list, target_file_list):
    """
    获取没有成功添加扰动的音频
    :param source_file_list:
    :param target_file_list:
    :return:
    """
    error_list = []
    i = 0
    j = 0
    while i < len(source_file_list) and j < len(target_file_list):
        if source_file_list[i][0:source_file_list[i].rfind(".")] in target_file_list[j]:
            i += 1
            j += 1
        else:
            error_list.append(source_file_list[i])
            i += 1
    while i < len(source_file_list):
        error_list.append(source_file_list[i])
        i += 1
    return error_list


def get_order_number(name):
    """
    获取文件名中的序号
    :param name:
    :return:
    """
    return re.findall("\\d+", name)[0]


def if_duplicate(dataset):
    """
    查看添加扰动后的音频列表是否因错误而重复添加
    :param dataset: cv-corpus-chinese or timit
    :return:
    """
    duplicate_list = []
    data = {}
    from Dataset.DatasetList import get_dataset_instance
    dataset_instance = get_dataset_instance(dataset)
    noise_clips = dataset_instance.get_noise_audio_clips_list()
    for clip in noise_clips:
        name, pattern_tag = dataset_instance.get_name_and_pattern_tag(clip)
        if name in data.keys():
            data[name] = data[name] + 1
        else:
            data[name] = 1
    for key, value in data.items():
        if value >= 2:
            duplicate_list.append(key)
    return duplicate_list


def get_audio_form(audio_name):
    """
    获取音频格式
    :param audio_name: X/X/X/XXXXX.wav
    :return:
    """
    return audio_name[audio_name.rindex('.') + 1:]


def get_str_n_find(string, target_str, num):
    """
    找到target_str在string中第num次出现的位置
    :param string:
    :param target_str:
    :param num:
    :return:
    """
    pos = -1
    while num > 0:
        pos = string.find(target_str, pos + 1)
        if pos == -1:
            return -1
        num = num - 1
    return pos
