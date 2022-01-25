import librosa
import soundfile

from Perturbation.AudioProcess import *
from Util.RpcResult import RpcResult
from Util.util import *


def add_gaussian_noise(path, audioName):
    """
    添加高斯白噪声
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :return:
    """
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = gaussian_white_noise(sig, snr=5)
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    waveName = audioName.replace(".mp3", ".wav")
    noiseWaveName = addTag(waveName, "gaussian_white_noise")
    soundfile.write(wavePath + noiseWaveName, noiseAudio, sr)
    trans_wav_to_mp3(wavePath, noiseWaveName)
    removeAudio(wavePath, noiseWaveName)
    return RpcResult.ok("")


def add_sound_level(path, audioName, specificPattern):
    """
    添加 sound level 扰动
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :param specificPattern: 具体扰动 {louder:更响,quieter:更静,pitch:英高,speed:变速（更快）}
    :return:
    """
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = sig
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    if specificPattern == "Louder":
        noiseAudio = louder(sig)
    elif specificPattern == "Quieter":
        noiseAudio = quieter(sig)
    elif specificPattern == "Pitch":
        noiseAudio = changePitch(sig, sr)
    elif specificPattern == "Speed":
        sr = sr * 2
    noiseWaveName = addTag(addTag(audioName, "sound_level"),
                           patternTypeToSuffix(specificPattern)).replace(".mp3", ".wav")
    soundfile.write(wavePath + noiseWaveName, noiseAudio, sr)
    trans_wav_to_mp3(wavePath, noiseWaveName)
    removeAudio(wavePath, noiseWaveName)
    return RpcResult.ok("")


def add_natural_sounds(path, audioName, specificPattern):
    """
    添加 natural sound 扰动
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :param specificPattern:
    :return:
    """
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = sig
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    # todo 声音还是有点小
    if specificPattern == "Wind":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Natural Sounds/winds.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Thunderstorm":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Natural Sounds/thunderstorm.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Water":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Natural Sounds/water.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Fire":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Natural Sounds/fire.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    noiseWaveName = addTag(addTag(audioName, "natural_sounds"), patternTypeToSuffix(specificPattern)).replace(".mp3",
                                                                                                              ".wav")
    soundfile.write(wavePath + noiseWaveName, noiseAudio, sr)
    trans_wav_to_mp3(wavePath, noiseWaveName)
    removeAudio(wavePath, noiseWaveName)
    return RpcResult.ok("")


if __name__ == '__main__':
    # sig, sr = librosa.load(r"D:\AudioSystem\Noise\Natural Sounds\winds.mp3", sr=None)
    # sig = sig * 10
    # soundfile.write(r"D:\AudioSystem\Noise\Natural Sounds\winds10.wav", sig, sr)
    add_natural_sounds("D:/AudioSystem/Audio/cv-corpus-chinese/clips/", "common_voice_zh-CN_18524189.mp3",
                       "Water")
