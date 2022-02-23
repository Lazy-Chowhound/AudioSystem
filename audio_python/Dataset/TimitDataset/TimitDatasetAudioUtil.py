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
