import jiwer


def wer(r, h):
    """
    计算 WER，用于英文
    :param r: 真实的 I am going to eat lunch
    :param h: 预测的 She is going to eat supper
    :return:
    """
    return jiwer.wer(r, h)


def cer(r, h):
    """
    计算 CER，用于中文
    :param r: 真实的 她马上要去吃午饭
    :param h: 推测的 我要去吃晚饭了
    :return:
    """
    return jiwer.cer(r, h)


def wer_overall(r_list: list, h_list: list):
    """
    整个数据集的 WER
    :param r_list:
    :param h_list:
    :return:
    """
    return jiwer.wer(r_list, h_list)


def cer_overall(r_list: list, h_list: list):
    """
    整个数据集的 CER
    :param r_list:
    :param h_list:
    :return:
    """
    return jiwer.cer(r_list, h_list)
