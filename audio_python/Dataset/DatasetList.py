from Dataset.AiShell.AiShell import AiShell
from Dataset.CommonVoice.CommonVoice import CommonVoice
from Dataset.Thchs30.Thchs30 import Thchs30
from Dataset.Timit.Timit import Timit

dataset_list = ["cv-corpus-chinese", "timit"]


def get_dataset_instance(dataset):
    """
    根据数据集名称返回实例
    :param dataset:
    :return:
    """
    if dataset == "cv-corpus-chinese":
        return CommonVoice("cv-corpus-chinese")
    elif dataset == "cv-corpus-deutsch":
        return CommonVoice("cv-corpus-deutsch")
    elif dataset == "cv-corpus-japanese":
        return CommonVoice("cv-corpus-japanese")
    elif dataset == "timit":
        return Timit("timit")
    elif dataset == "data_aishell":
        return AiShell("data_aishell")
    elif dataset == "data_thchs30":
        return Thchs30("data_thchs30")
