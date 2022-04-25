import glob
import os.path

from sphfile import SPHFile

from Util.AudioUtil import AUDIO_SETS_PATH


def trans_WAV_to_wav():
    """
    TIMIT 生成 wav 文件
    :return:
    """
    wav_file = AUDIO_SETS_PATH + "timit/lisa/data/timit/raw/TIMIT/*/*/*/*.WAV"
    sph_files = glob.glob(wav_file)
    for sph_file in sph_files:
        sph = SPHFile(sph_file)
        print(sph_file + " has transform to " + sph_file.replace(".WAV", "_n.wav"))
        sph.write_wav(sph_file.replace(".WAV", "_n.wav"))


def make_noise_audio_clips_dirs(path):
    """
    根据文件路径，生成所需文件夹
    :param path: D:/AudioSystem/NoiseAudio/timit/lisa/data/timit/raw/TIMIT/TRAIN/DR1/FCJF0
                /SA1_n_gaussian_white_noise.wav
    :return:
    """
    noise_audio_dir = path[0:path.rfind("/")]
    if not os.path.exists(noise_audio_dir):
        os.makedirs(noise_audio_dir)


def get_error_audio_dirs():
    """
    获取有重复添加扰动的文件夹
    :return: 
    """
    from Util.AudioUtil import if_duplicate
    dup_list = if_duplicate("timit")
    s = {}
    for audio in dup_list:
        directory = audio[0:audio.rfind("/") + 1]
        if directory not in s.keys():
            s[directory] = 1
    directories = []
    for key in s.keys():
        directories.append(key)
    return directories


def remove_duplicate_audios():
    """
    删除重复添加扰动的音频
    :return:
    """
    path = "D:/AudioSystem/NoiseAudio/timit/lisa/data/timit/raw/TIMIT/"
    for audio_dir in get_error_audio_dirs():
        audios = os.listdir(path + audio_dir)
        data = {}
        for audio in audios:
            name = audio[0:audio.find("_n") + 2]
            if name in data.keys():
                data[name].append(audio)
            else:
                data[name] = [audio]
        for key, value in data.items():
            if len(value) >= 2:
                for x in range(1, len(value)):
                    os.remove(path + audio_dir + value[x])
