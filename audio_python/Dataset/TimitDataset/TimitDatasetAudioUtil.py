import glob

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