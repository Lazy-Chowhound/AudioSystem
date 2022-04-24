import os

from Dataset import DatasetList
from Dataset.AiShell.AiShell import AiShell
from Dataset.TimitDataset.TimitDataset import TimitDataset
from Perturbation.NoisePatternAddition import add_pertubation_test_set


def get_not_10_timit_noise_dirs():
    res = []
    path = "D:/AudioSystem/NoiseAudio/timit/lisa/data/timit/raw/TIMIT/TEST/"
    for file in os.listdir(path):
        for nextfile in os.listdir(path + file):
            if len(os.listdir(path + file + "/" + nextfile)) != 10:
                res.append(path + file + "/" + nextfile)
    return res


def get_duplicate_add_noise_clips():
    td = TimitDataset("timit")

    r = td.get_noise_audio_clips_list()
    s = set()
    for item in r:
        s.add(item[0:item.find("_n") + 2])
    print(len(s))


def get_real_text(order, start, end, dataset, directory):
    """
    将原音频内容写入txt
    :param order: 序号
    :param start: 开始音频序号
    :param end: 结束音频序号
    :param dataset: 数据集名
    :param directory: 路径
    :return:
    """
    dataset_instance = DatasetList.get_dataset_instance(dataset)
    test_list = dataset_instance.get_testset_audio_clips_list()
    error_list = []
    if end == -1:
        end = len(test_list)
    for audio in test_list[start:end]:
        try:
            with open(directory + r"\realText" + str(order) + ".txt", "a", encoding="utf-8") as f:
                txt = dataset_instance.get_audio_clip_content(audio)
                txt = dataset_instance.formalize(txt)
                f.writelines(audio + " " + txt + "\n")
        except Exception:
            error_list.append(audio)
    print(error_list)


def get_clean_text(order, model, start, end, dataset, directory):
    """
    将原音频识别出的内容写入txt
    :param order: 序号
    :param model: 模型名
    :param start: 开始音频序号
    :param end: 结束音频序号
    :param dataset: 数据集名
    :param directory: 路径
    :return:
    """
    dataset_instance = DatasetList.get_dataset_instance(dataset)
    test_list = dataset_instance.get_testset_audio_clips_list()
    if not dataset_instance.judge_model(model):
        print("模型错误")
    dataset_instance.load_model(model)
    error_list = []
    if end == -1:
        end = len(test_list)
    for audio in test_list[start:end]:
        try:
            with open(directory + r"\previousText" + str(order) + ".txt", "a", encoding="utf-8") as f:
                txt = dataset_instance.get_audio_clip_transcription(audio, model)
                txt = dataset_instance.formalize(txt)
                f.writelines(audio + " " + txt + "\n")
        except Exception:
            error_list.append(audio)
    print(error_list)


def get_noise_text(order, model, start, end, dataset, directory):
    """
    将扰动音频识别出的内容写入txt
    :param order: 序号
    :param model: 模型名
    :param start: 开始音频序号
    :param end: 结束音频序号
    :param dataset: 数据集名
    :param directory: 路径
    :return:
    """
    dataset_instance = DatasetList.get_dataset_instance(dataset)
    test_list = dataset_instance.get_testset_audio_clips_list()
    dataset_instance.load_model(model)
    if not dataset_instance.judge_model(model):
        print("模型错误")
    error_list = []
    if end == -1:
        end = len(test_list)
    for audio in test_list[start:end]:
        try:
            with open(directory + r"\postText" + str(order) + ".txt", "a", encoding="utf-8") as f:
                noise_audio = dataset_instance.get_noise_clip_name(audio)
                txt = dataset_instance.get_noise_audio_clip_transcription(noise_audio, model)
                txt = dataset_instance.formalize(txt)
                f.writelines(audio + " " + txt + "\n")
        except Exception:
            error_list.append(audio)
    print(error_list)


def get_text_list(path, dataset):
    """
    将txt中的文本插入列表
    :param path: txt路径
    :param dataset: 数据集名
    :return:
    """
    dataset_instance = DatasetList.get_dataset_instance(dataset)
    res = []
    with open(path, "r", encoding="utf-8") as f:
        realText_list = f.read().splitlines()
        for item in realText_list:
            res.append(dataset_instance.formalize(item.split(" ", 1)[1]))
    return res


if __name__ == '__main__':
    add_pertubation_test_set("data_aishell", 8)
