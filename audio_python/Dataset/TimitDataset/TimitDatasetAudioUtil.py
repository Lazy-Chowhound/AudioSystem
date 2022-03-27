import glob
import json
import os.path

from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube
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


def download_video_from_Youtube(url, path):
    """
    从Youtube上下载视频
    :param url: 视频地址
    :param path: 下载目录
    :return:
    """
    yt = YouTube(url)
    yt.streams.filter(file_extension="mp4").first().download(path)


def extract_audio(source_path, start, end, pattern_type, target_path):
    """
    从视频中提取音频
    :param source_path:
    :param start: 开始的秒数
    :param end: 结束的秒数
    :param pattern_type:
    :param target_path: 输出路径 形如 C:/Users/Nakano Miku/Desktop/audio/
    :return:
    """
    audio_background = AudioFileClip(source_path).subclip(start, end)
    audio_background.write_audiofile(target_path + pattern_type + ".wav", fps=48000)


def load_ontology(path="C:/Users/Nakano Miku/Desktop/毕业论文/资料/ontology-master/ontology.json"):
    """
    加载 json 文件
    :param path: json文件地址
    :return:
    """
    with open(path, 'r', encoding='utf8') as f:
        json_data = json.load(f)
    return json_data


def get_json_from_id(json_id, json_data):
    """
    根据id获取json字典
    :param json_id:
    :param json_data:
    :return:
    """
    for item in json_data:
        if json_id == item['id']:
            return item


def get_child(url_dict: dict, item: dict, name, json_data):
    """
    递归获取所有子孩子下的 url
    :param url_dict: url字典
    :param item: 当前json字典
    :param name: 名称
    :param json_data: 原始json
    :return:
    """
    examples = item['positive_examples']
    if len(name) == 0:
        cur_name = item['name']
    else:
        cur_name = name + "_" + item['name']
    if len(examples) != 0:
        if cur_name not in url_dict.keys():
            url_dict[cur_name] = []
        for ex in examples:
            url_dict[cur_name].append(ex)
    children = item['child_ids']
    if len(children) != 0:
        for child in children:
            child_item = get_json_from_id(child, json_data)
            get_child(url_dict, child_item, cur_name, json_data)


def get_url_dict():
    url_dict = {}
    json_data = load_ontology()
    categories = ["Human sounds", "Animal", "Natural sounds", "Source-ambiguous sounds", "Sounds of things", "Music"]
    for category in categories:
        for item in json_data:
            if item['name'] == category:
                get_child(url_dict, item, "", json_data)
    return url_dict
