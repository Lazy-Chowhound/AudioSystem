from Dataset.CommonVoiceDataset.CommonVoiceDataset import CommonVoiceDataset
from Dataset.TimitDataset.TimitDataset import TimitDataset

dataset_list = ["cv-corpus-chinese", "timit"]


def get_dataset_instance(dataset):
    """
    根据数据集名称返回实例
    :param dataset:
    :return:
    """
    if dataset == "cv-corpus-chinese":
        return CommonVoiceDataset("cv-corpus-chinese")
    elif dataset == "cv-corpus-deutsch":
        return CommonVoiceDataset("cv-corpus-deutsch")
    elif dataset == "cv-corpus-japanese":
        return CommonVoiceDataset("cv-corpus-japanese")
    elif dataset == "timit":
        return TimitDataset("timit")
