import logging
import threading
from multiprocessing import Pool

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
    if specificPattern in natural_sounds_specificPatterns:
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
    if specificPattern in animal_specificPatterns:
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
    if specificPattern in sound_of_things_specificPatterns:
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
    if specificPattern in human_sounds_specificPatterns:
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
    if specificPattern in music_specificPatterns:
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
    if specificPattern in source_ambiguous_sounds_specificPatterns:
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/Source-ambiguous sounds/" + specificPattern + ".wav",
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


def add_randomly_multiProcess(path):
    """
    多线程添加扰动
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :return:
    """
    logging.basicConfig(level=logging.ERROR, filename="error.log", filemode="a",
                        format="%(levelname)s %(asctime)s %(filename)s %(message)s")
    PROCESS_NUM = 8
    audio_list = []
    for root, dirs, files in os.walk(path):
        audio_list = files
    task_slice = math.ceil(len(audio_list) / PROCESS_NUM)

    pool = Pool(PROCESS_NUM)
    for i in range(0, PROCESS_NUM):
        pool.apply_async(add_pattern_range,
                         args=(path, audio_list, i * task_slice,
                               min((i + 1) * task_slice - 1, len(audio_list) - 1),))
    pool.close()
    pool.join()


def add_pattern_range(path, audio_list, start, end):
    """
    范围添加扰动
    :param path:
    :param audio_list:
    :param start:
    :param end:
    :return:
    """
    print('process %s working...' % (os.getpid()))
    for audio in audio_list[start:end]:
        add_pattern_randomly(path, audio)


def add_pattern_randomly(path, file):
    """
    随即个某一音频添加噪声
    :param path: 形如 D:/AudioSystem/Audio/cv-corpus-chinese/clips/
    :param file: common_voice_zh-CN_18524189.mp3
    :return:
    """
    try:
        p = random.randint(1, 8)
        if p == 1:
            add_gaussian_noise(path, file)
        elif p == 2:
            ptype = sound_level_specificPatterns
            add_sound_level(path, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 3:
            ptype = animal_specificPatterns
            add_animal(path, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 4:
            ptype = sound_of_things_specificPatterns
            add_sound_of_things(path, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 5:
            ptype = human_sounds_specificPatterns
            add_human_sounds(path, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 6:
            ptype = natural_sounds_specificPatterns
            add_natural_sounds(path, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 7:
            ptype = music_specificPatterns
            add_music(path, file, ptype[random.randint(0, len(ptype) - 1)])
        elif p == 8:
            ptype = source_ambiguous_sounds_specificPatterns
            add_source_ambiguous_sounds(path, file, ptype[random.randint(0, len(ptype) - 1)])
        print(path + file + " finished")
    except Exception as e:
        logging.warning(path + file + " fail ", e)


if __name__ == "__main__":
    add_randomly_multiProcess("D:/AudioSystem/Audio/cv-corpus-arabic/clips")
    add_randomly_multiProcess("D:/AudioSystem/Audio/cv-corpus-chinese/clips")
    add_randomly_multiProcess("D:/AudioSystem/Audio/cv-corpus-portuguese/clips")
    add_randomly_multiProcess("D:/AudioSystem/Audio/cv-corpus-russian/clips")
