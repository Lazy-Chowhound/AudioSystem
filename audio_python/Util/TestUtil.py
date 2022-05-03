import shutil

from Dataset import DatasetList
from Dataset.DatasetList import get_dataset_instance


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


def move_test_set_audio_clips(dataset, path):
    dataset_instance = get_dataset_instance(dataset)
    test_audios = dataset_instance.get_testset_audio_clips_list()
    for audio in test_audios:
        shutil.copy(dataset_instance.clips_path + audio, path)
        print(audio + "已拷贝到" + path)
