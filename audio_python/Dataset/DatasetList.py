from Dataset.AiShell.AiShell import AiShell
from Dataset.CommonVoice.CommonVoice import CommonVoice
from Dataset.JSUT.JSUT import JSUT
from Dataset.LibriSpeech.LibriSpeech import LibriSpeech
from Dataset.TUDA.TUDA import TUDA
from Dataset.Thchs30.Thchs30 import Thchs30
from Dataset.Timit.Timit import Timit

dataset_list = ["cv-corpus-chinese", "timit", "data_aishell",
                "data_thchs30", "german-speechdata-package-v2", "jsut",
                "librispeech"]


def get_dataset_instance(dataset):
    """
    根据数据集名称返回实例
    :param dataset:
    :return:
    """
    if dataset.startswith("cv-corpus"):
        return CommonVoice(dataset)
    elif dataset == "timit":
        return Timit(dataset)
    elif dataset == "data_aishell":
        return AiShell(dataset)
    elif dataset == "data_thchs30":
        return Thchs30(dataset)
    elif dataset == "german-speechdata-package-v2":
        return TUDA(dataset)
    elif dataset == "jsut":
        return JSUT(dataset)
    elif dataset == "librispeech":
        return LibriSpeech(dataset)
