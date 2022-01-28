import soundfile

from Perturbation.AudioProcess import *
from Util.Annotation import rpcApi
from Util.AudioUtil import *
from Util.RpcResult import RpcResult


@rpcApi
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
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
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
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
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
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_animal(path, audioName, specificPattern):
    """
    添加 animal 扰动
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :param specificPattern:
    :return:
    """
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = sig
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    if specificPattern == "Pet":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/pet.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Livestock":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/livestock.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Wild animals":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/wild animals.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    noiseWaveName = addTag(addTag(audioName, "animal"),
                           patternTypeToSuffix(specificPattern)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_sound_of_things(path, audioName, specificPattern):
    """
    添加 sound of things 扰动
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :param specificPattern:
    :return:
    """
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = sig
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    if specificPattern == "Vehicle":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/vehicle.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Engine":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/engine.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "":
        pass
    elif specificPattern == "Bell":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/bell.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Alarm":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/alarm.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Mechanisms":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/mechanism.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Explosions":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/explosion.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Wood":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Glass":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Liquid":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/liquid.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "":
        pass
    elif specificPattern == "":
        pass
    noiseWaveName = addTag(addTag(audioName, "sound_of_things"),
                           patternTypeToSuffix(specificPattern)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_human_sounds(path, audioName, specificPattern):
    """
    添加 human sounds 扰动
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :param specificPattern:
    :return:
    """
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = sig
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    if specificPattern == "":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Human Sounds/", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Whistling":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Human Sounds/whistle.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Respiratory sounds":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Human Sounds/respiratory sounds.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Human locomotion":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Human Sounds/locomotion.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Hands":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Human Sounds/hands.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Heartbeat":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Human Sounds/heartbeat.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Human group actions":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Human Sounds/group actions.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    noiseWaveName = addTag(addTag(audioName, "human_sounds"),
                           patternTypeToSuffix(specificPattern)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_music(path, audioName, specificPattern):
    """
    添加 music 扰动
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :param specificPattern:
    :return:
    """
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = sig
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    if specificPattern == "Music instrument":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/pet.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Music genre":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/livestock.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Music concepts":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/wild animals.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Music role":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/wild animals.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Music mood":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/wild animals.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    noiseWaveName = addTag(addTag(audioName, "animal"),
                           patternTypeToSuffix(specificPattern)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_source_ambiguous_sounds(path, audioName, specificPattern):
    """
    添加 source_ambiguous_sounds 扰动
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param audioName: 形如 common_voice_zh-CN_18524189.mp3
    :param specificPattern:
    :return:
    """
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = sig
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    if specificPattern == "Generic impact sounds":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Surface contact":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/livestock.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Deformable shell":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/wild animals.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    elif specificPattern == "Onomatopoeia":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/wild animals.wav", sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    noiseWaveName = addTag(addTag(audioName, "animal"),
                           patternTypeToSuffix(specificPattern)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


def writeNoiseAudio(path, noiseAudioName, noiseAudio, sr):
    """
    将生成的扰动噪音以 wav 形式写入，然后转为 mp3 格式 然后删除原 wav
    :param path: 写入的地址
    :param noiseAudioName: 生成的音频文件名
    :param noiseAudio: 音频数据
    :param sr: 采样率
    :return:
    """
    soundfile.write(path + noiseAudioName, noiseAudio, sr)
    trans_wav_to_mp3(path, noiseAudioName)
    removeAudio(path, noiseAudioName)


if __name__ == '__main__':
    add_animal("D:/AudioSystem/Audio/cv-corpus-chinese/clips/", "common_voice_zh-CN_18524189.mp3",
               "Wild animals")
    add_animal("D:/AudioSystem/Audio/cv-corpus-chinese/clips/", "common_voice_zh-CN_18524189.mp3",
               "Livestock")
