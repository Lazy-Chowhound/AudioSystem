import os

from pydub import AudioSegment


def trans_mp3_to_wav(path, audioName):
    """
    mp3转wav
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
    wav转mp3
    :param path: 形如 D:/AudioSystem/noiseAudio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189_gaussian_white_noise.wav
    :return: 生成的 wav 地址
    """
    audio = AudioSegment.from_wav(path + audioName)
    audioName = audioName.replace(".wav", ".mp3")
    audio.export(path + audioName, format="mp3")
    return path, audioName


if __name__ == '__main__':
    pass
