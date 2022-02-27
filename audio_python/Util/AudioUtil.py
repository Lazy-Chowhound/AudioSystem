import re

import librosa
import soundfile
from moviepy.audio.io.AudioFileClip import AudioFileClip

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

sound_level_pattern_types = ["Louder", "Quieter", "Pitch", "Speed"]

animal_pattern_types = ["Pets", "Livestock", "Wild animals"]

sound_of_things_pattern_types = ["Vehicle", "Engine", "Domestic sounds", "Bell", "Alarm", "Mechanisms", "Explosion",
                                 "Wood", "Glass", "Liquid", "Miscellaneous sources", "Specific impact sounds"]

human_sounds_pattern_types = ["Human voice", "Whistling", "Respiratory sounds", "Human locomotion", "Hands",
                              "Heartbeat", "Human group actions"]

natural_sounds_pattern_types = ["Wind", "Thunderstorm", "Water", "Fire"]

music_pattern_types = ["Musical instrument", "Music genre", "Musical concepts", "Music role", "Music mood"]

source_ambiguous_sounds_pattern_types = ["Generic impact sounds", "Surface contact", "Deformable shell",
                                         "Onomatopoeia", "Silence", "Other sourceless"]


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


def get_pattern_info_from_name(pattern_tag):
    """
    从名称后缀解析出扰动大类和具体类型
    :param pattern_tag: animal_wild_animals
    :return: animal,wild animals
    """
    if "gaussian_white_noise" in pattern_tag:
        return name_to_pattern["gaussian_white_noise"], suffix_to_pattern_type("gaussian_white_noise")
    else:
        for key, value in name_to_pattern.items():
            if key in pattern_tag:
                return name_to_pattern[key], suffix_to_pattern_type(pattern_tag.replace(key + "_", ""))


def get_source_noises_path(pattern, pattern_type):
    return SOURCE_NOISES_PATH + pattern + "/" + pattern_type + ".wav"


def extract_audio(source_path, start, end, pattern_type, target_path):
    """
    从视频中提取音频
    :param source_path:
    :param start: 开始的秒数
    :param end: 结束的秒数
    :param pattern_type:
    :param target_path: 输出路径 形如 C:/Users/Nakano Miku/Desktop/audio/
    :return:
    """
    audio_background = AudioFileClip(source_path).subclip(start, end)
    audio_background.write_audiofile(target_path + pattern_type + ".wav", fps=48000)


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


def get_error_audio_clips(dataset):
    """
    获取没有成功添加扰动的音频
    :param dataset: cv-corpus-chinese or timit
    :return:
    """
    from Dataset.DatasetList import get_dataset_instance
    dataset_instance = get_dataset_instance(dataset)
    error_list = []
    source_file_list = dataset_instance.get_audio_clips_list()
    target_file_list = dataset_instance.get_noise_audio_clips_list()

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


if __name__ == '__main__':
    pass
