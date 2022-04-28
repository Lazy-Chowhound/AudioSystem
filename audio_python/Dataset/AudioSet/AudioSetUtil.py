import json

from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube


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
    :param json_id: json数据的id
    :param json_data: 原json数据
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
