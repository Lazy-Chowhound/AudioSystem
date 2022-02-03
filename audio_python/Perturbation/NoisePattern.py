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
    else:
        return RpcResult.error("patternType error")
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
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    specificPatterns = ["Wind", "Thunderstorm", "Water", "Fire"]
    if specificPattern in specificPatterns:
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Natural Sounds/" + specificPattern + ".wav", sr=sr,
                                          mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = addTag(addTag(audioName, "natural_sounds"),
                           patternTypeToSuffix(specificPattern)).replace(".mp3", ".wav")
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
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    specificPatterns = ["Pets", "Livestock", "Wild animals"]
    if specificPattern in specificPatterns:
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Animal/" + specificPattern + ".wav", sr=sr,
                                          mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
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
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    specificPatterns = ["Vehicle", "Engine", "Domestic sounds", "Bell", "Alarm", "Mechanisms", "Explosions", "Wood",
                        "Glass", "Liquid", "Miscellaneous sources", ""]
    if specificPattern in specificPatterns:
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Sound of things/" + specificPattern + ".wav", sr=sr,
                                          mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
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
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    specificPatterns = ["Human voice", "Whistling", "Respiratory sounds", "Human locomotion", "Hands", "Heartbeat",
                        "Human group actions"]
    if specificPattern in specificPatterns:
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Human Sounds/" + specificPattern + ".wav", sr=sr,
                                          mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
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
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    specificPatterns = ["Musical instrument", "Music genre", "Musical concepts", "Music role", "Music mood"]
    if specificPattern in specificPatterns:
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Music/" + specificPattern + ".wav", sr=sr,
                                          mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = addTag(addTag(audioName, "music"),
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
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    specificPatterns = ["Generic impact sounds", "Surface contact", "Deformable shell", "Onomatopoeia", "Silence",
                        "Other sourceless"]
    if specificPattern in specificPatterns:
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Source-ambiguous sounds" + specificPattern + ".wav",
                                          sr=sr, mono=True)
        noiseAudio = addNoise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = addTag(addTag(audioName, "source_ambiguous_sounds"),
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
               "Pet")
