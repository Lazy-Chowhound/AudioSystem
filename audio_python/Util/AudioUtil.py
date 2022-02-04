import os
import re

import librosa
import soundfile
from moviepy.editor import *
from pydub import AudioSegment

patternToName = {"Gaussian noise": "gaussian_white_noise",
                 "Sound level": "sound_level",
                 "Animal": "animal",
                 "Source-ambiguous sounds": "source_ambiguous_sounds",
                 "Natural sounds": "natural_sounds",
                 "Sound of things": "sound_of_things",
                 "Human sounds": "human_sounds",
                 "Music": "music"}

nameToPattern = {"gaussian_white_noise": "Gaussian noise",
                 "sound_level": "Sound level",
                 "animal": "Animal",
                 "source_ambiguous_sounds": "Source-ambiguous sounds",
                 "natural_sounds": "Natural sounds",
                 "sound_of_things": "Sound of things",
                 "human_sounds": "Human sounds",
                 "music": "Music"}

sound_level_specificPatterns = ["Louder", "Quieter", "Pitch", "Speed"]
animal_specificPatterns = ["Pets", "Livestock", "Wild animals"]
sound_of_things_specificPatterns = ["Vehicle", "Engine", "Domestic sounds", "Bell", "Alarm", "Mechanisms", "Explosion",
                                    "Wood", "Glass", "Liquid", "Miscellaneous sources", "Specific impact sounds"]
human_sounds_specificPatterns = ["Human voice", "Whistling", "Respiratory sounds", "Human locomotion", "Hands",
                                 "Heartbeat", "Human group actions"]
natural_sounds_specificPatterns = ["Wind", "Thunderstorm", "Water", "Fire"]
music_specificPatterns = ["Musical instrument", "Music genre", "Musical concepts", "Music role", "Music mood"]
source_ambiguous_sounds_specificPatterns = ["Generic impact sounds", "Surface contact", "Deformable shell",
                                            "Onomatopoeia", "Silence", "Other sourceless"]


def trans_mp3_to_wav(path, audioName):
    """
    mp3转 wav
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :return: 生成的 wav 地址
    """
    audio = AudioSegment.from_mp3(path + audioName)
    targetPath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)
    audioName = audioName.replace(".mp3", ".wav")
    audio.export(targetPath + audioName, format="wav")
    return targetPath, audioName


def trans_wav_to_mp3(path, audioName):
    """
    wav转 mp3
    :param path: 形如 D:/AudioSystem/noiseAudio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189_gaussian_white_noise.wav
    :return: 生成的 wav 地址
    """
    audio = AudioSegment.from_wav(path + audioName)
    audioName = audioName.replace(".wav", ".mp3")
    audio.export(path + audioName, format="mp3")
    return path, audioName


def addTag(name, tag):
    """
    给添加扰动后生成的文件名打上对应扰动的类型
    :param name:
    :param tag:
    :return:
    """
    pos = name.index(".")
    return name[0:pos] + "_" + tag + name[pos:]


def suffixToPatternType(suffix):
    """
    将音频名称扰动后缀转换为对应的扰动类型
    gaussian_white_noise ---> Gaussian white noise
    :param suffix:
    :return:
    """
    return suffix.replace("_", " ").capitalize()


def patternTypeToSuffix(patternType):
    """
    扰动类型转换为对应后缀
    Gaussian white noise ---> gaussian_white_noise
    :param patternType:
    :return:
    """
    return patternType.replace(" ", "_").lower()


def removeAudio(path, audioName):
    """
    删除音频
    :param path:
    :param audioName:
    :return:
    """
    os.remove(path + audioName)


def getPatternInfo(patternTag):
    """
    从名称后缀解析出扰动大类和具体类型
    animal_wild_animals ---> animal,wild animals
    :param patternTag:
    :return:
    """
    if "gaussian_white_noise" in patternTag:
        return nameToPattern["gaussian_white_noise"], suffixToPatternType("gaussian_white_noise")
    else:
        for key, value in nameToPattern.items():
            if key in patternTag:
                return nameToPattern[key], suffixToPatternType(patternTag.replace(key + "_", ""))


def extractAudio(path, start, end, patternType):
    """
    从视频中提取音频
    :param path:
    :param start: 开始的秒数
    :param end: 结束的秒数
    :param patternType:
    :return:
    """
    audio_background = AudioFileClip(path).subclip(start, end)
    audio_background.write_audiofile("C:/Users/Nakano Miku/Desktop/audio/" + patternType + ".wav", fps=48000)


def cutAudio(path, start, end=None):
    """
    截取音频
    :param path:
    :param start: 开始的秒数
    :param end: 结束的秒数
    :return:
    """
    sig, sr = librosa.load(path, sr=None)
    if end is None:
        audio_dst = sig[start * sr:]
    else:
        audio_dst = sig[start * sr:end * sr]
    soundfile.write(path[0: path.find(".")] + "_cut" + ".wav", audio_dst, sr)


def find_error_audio(dataset):
    """
    寻找没有成功添加的音频
    :param dataset: cv-corpus-chinese
    :return: 
    """
    error_list = []
    source_path = "D:/AudioSystem/Audio/" + dataset + "/clips/"
    target_path = "D:/AudioSystem/NoiseAudio/" + dataset + "/clips/"
    source_file_list = []
    target_file_list = []
    for root, dirs, files in os.walk(source_path):
        source_file_list = files
    for root, dirs, files in os.walk(target_path):
        target_file_list = files
    for audio in source_file_list:
        number = audio[audio.rfind("_") + 1:audio.find(".")]
        flag = False
        for t_audio in target_file_list:
            if number in t_audio:
                flag = True
                break
        if flag is False:
            error_list.append(audio)
    return error_list


def extract_error_audio_from_log():
    """
    从 log 中提取出错的 audio
    :return:
    """
    path = "D:/AudioSystem/audio_python/Perturbation/error.log"
    error_list = []
    with open(path) as f:
        while True:
            lines = f.readline()
            if not lines:
                break
            line = lines.split(" ")
            error_list.append(line[4][line[4].rfind("/") + 1:])
    return error_list


def getOrder(name):
    """
    获取文件名中的序号
    :param name:
    :return:
    """
    return re.findall("\\d+", name)[0]


def ifDuplicate(path):
    """
    查看添加扰动后的音频列表是否因错误而重复添加
    :param path: D:/AudioSystem/NoiseAudio/cv-corpus-japanese/clips
    :return: 
    """
    duplicate_list = []
    data = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            order = getOrder(file)
            if order in data.keys():
                data[order] = data[order] + 1
            else:
                data[order] = 1
    for key, value in data.items():
        if value >= 2:
            duplicate_list.append(key)
    return duplicate_list


if __name__ == '__main__':
    pass
