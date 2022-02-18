import logging
from multiprocessing import Pool

from Perturbation.AudioProcess import *
from Util.Annotation import rpcApi
from Util.AudioUtil import *
from Util.RpcResult import RpcResult


@rpcApi
def add_gaussian_noise(dataset, audio_name):
    """
    添加高斯白噪声
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :return:
    """
    path = get_audio_clips_path(dataset)
    sig, sr = librosa.load(path + audio_name, sr=None)
    noiseAudio = gaussian_white_noise(sig, snr=5)
    wavePath = get_noise_audio_clips_path(dataset)
    waveName = audio_name.replace(".mp3", ".wav")
    noiseWaveName = add_tag(waveName, "gaussian_white_noise")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_sound_level(dataset, audio_name, pattern_type):
    """
    添加 sound level 扰动
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :param pattern_type: 具体扰动 {louder:更响,quieter:更静,pitch:英高,speed:变速（更快）}
    :return:
    """
    path = get_audio_clips_path(dataset)
    sig, sr = librosa.load(path + audio_name, sr=None)
    noiseAudio = sig
    wavePath = get_noise_audio_clips_path(dataset)
    if pattern_type == "Louder":
        noiseAudio = louder(sig)
    elif pattern_type == "Quieter":
        noiseAudio = quieter(sig)
    elif pattern_type == "Pitch":
        noiseAudio = change_pitch(sig, sr)
    elif pattern_type == "Speed":
        sr = sr * 2
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = add_tag(add_tag(audio_name, "sound_level"),
                            pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_natural_sounds(dataset, audio_name, pattern_type):
    """
    添加 natural sound 扰动
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :param pattern_type:
    :return:
    """
    path = get_audio_clips_path(dataset)
    sig, sr = librosa.load(path + audio_name, sr=None)
    wavePath = get_noise_audio_clips_path(dataset)
    if pattern_type in natural_sounds_pattern_types:
        noiseSig, noise_sr = librosa.load(get_source_noises_path("Natural Sounds", pattern_type), sr=sr, mono=True)
        noiseAudio = add_noise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = add_tag(add_tag(audio_name, "natural_sounds"),
                            pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_animal(dataset, audio_name, pattern_type):
    """
    添加 animal 扰动
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :param pattern_type:
    :return:
    """
    path = get_audio_clips_path(dataset)
    sig, sr = librosa.load(path + audio_name, sr=None)
    wavePath = get_noise_audio_clips_path(dataset)
    if pattern_type in animal_pattern_types:
        noiseSig, noise_sr = librosa.load(get_source_noises_path("Animal", pattern_type), sr=sr, mono=True)
        noiseAudio = add_noise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = add_tag(add_tag(audio_name, "animal"),
                            pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_sound_of_things(dataset, audio_name, pattern_type):
    """
    添加 sound of things 扰动
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :param pattern_type:
    :return:
    """
    path = get_audio_clips_path(dataset)
    sig, sr = librosa.load(path + audio_name, sr=None)
    wavePath = get_noise_audio_clips_path(dataset)
    if pattern_type in sound_of_things_pattern_types:
        noiseSig, noise_sr = librosa.load(get_source_noises_path("Sound of things", pattern_type), sr=sr, mono=True)
        noiseAudio = add_noise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = add_tag(add_tag(audio_name, "sound_of_things"),
                            pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_human_sounds(dataset, audio_name, pattern_type):
    """
    添加 human sounds 扰动
    :param dataset: cv-corpus-chinese
    :param audio_name: 形如 common_voice_zh-CN_18524189.mp3
    :param pattern_type:
    :return:
    """
    path = get_audio_clips_path(dataset)
    sig, sr = librosa.load(path + audio_name, sr=None)
    wavePath = get_noise_audio_clips_path(dataset)
    if pattern_type in human_sounds_pattern_types:
        noiseSig, noise_sr = librosa.load(get_source_noises_path("Human sounds", pattern_type), sr=sr, mono=True)
        noiseAudio = add_noise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = add_tag(add_tag(audio_name, "human_sounds"),
                            pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_music(dataset, audio_name, pattern_type):
    """
    添加 music 扰动
    :param dataset: cv-corpus-chinese
    :param audio_name: 形如 common_voice_zh-CN_18524189.mp3
    :param pattern_type:
    :return:
    """
    path = get_audio_clips_path(dataset)
    sig, sr = librosa.load(path + audio_name, sr=None)
    wavePath = get_noise_audio_clips_path(dataset)
    if pattern_type in music_pattern_types:
        noiseSig, noise_sr = librosa.load(get_source_noises_path("Music", pattern_type), sr=sr, mono=True)
        noiseAudio = add_noise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = add_tag(add_tag(audio_name, "music"),
                            pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


@rpcApi
def add_source_ambiguous_sounds(dataset, audio_name, pattern_type):
    """
    添加 source_ambiguous_sounds 扰动
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :param pattern_type:
    :return:
    """
    path = get_audio_clips_path(dataset)
    sig, sr = librosa.load(path + audio_name, sr=None)
    wavePath = get_noise_audio_clips_path(dataset)
    if pattern_type in source_ambiguous_sounds_pattern_types:
        noiseSig, noise_sr = librosa.load(get_source_noises_path("Source-ambiguous sounds", pattern_type), sr=sr,
                                          mono=True)
        noiseAudio = add_noise(sig, noiseSig)
    else:
        return RpcResult.error("patternType error")
    noiseWaveName = add_tag(add_tag(audio_name, "source_ambiguous_sounds"),
                            pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
    writeNoiseAudio(wavePath, noiseWaveName, noiseAudio, sr)
    return RpcResult.ok("")


def writeNoiseAudio(path, noise_audio_name, noiseAudio, sr):
    """
    将生成的扰动噪音以 wav 形式写入，然后转为 mp3 格式 然后删除原 wav
    :param path: 写入的地址
    :param noise_audio_name: 生成的音频文件名
    :param noiseAudio: 音频数据
    :param sr: 采样率
    :return:
    """
    soundfile.write(path + noise_audio_name, noiseAudio, sr)
    transform_wav_to_mp3(path, noise_audio_name)
    remove_audio(path, noise_audio_name)


def add_randomly_multiProcess(dataset, process_num):
    """
    多线程添加扰动
    :param process_num: 进程数
    :param dataset: cv-corpus-chinese
    :return:
    """
    logging.basicConfig(level=logging.ERROR, filename="error.log", filemode="a",
                        format="%(levelname)s %(asctime)s %(filename)s %(message)s")
    path = get_audio_clips_path(dataset)
    audio_list = []
    for root, dirs, files in os.walk(path):
        audio_list = files
    task_slice = math.ceil(len(audio_list) / process_num)

    pool = Pool(process_num)
    for i in range(0, process_num):
        pool.apply_async(add_pattern_range,
                         args=(dataset, audio_list, i * task_slice,
                               min((i + 1) * task_slice, len(audio_list)),))
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
    :param dataset: cv-corpus-chinese
    :param file: common_voice_zh-CN_18524189.mp3
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
    add_randomly_multiProcess("cv-corpus-test", 8)
