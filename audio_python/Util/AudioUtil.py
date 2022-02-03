import os

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
