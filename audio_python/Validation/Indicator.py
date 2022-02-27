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
    :param r: 真实的 他马上要去吃午饭
    :param h: 推测的 我要去吃晚饭了
    :return:
    """
    return jiwer.cer(r, h)


def wer_overall(r_list: list, h_list: list):
    """
    整个数据集的 WER
    :param r_list: ["i can spell", "i hope"]
    :param h_list: ["i kan cpell", "i hop"]
    :return:
    """
    return jiwer.wer(r_list, h_list)


def cer_overall(r_list: list, h_list: list):
    """
    整个数据集的 CER
    :param r_list: ["马上就来","你要去哪儿"]
    :param h_list: ["马上来","你要去那儿"]
    :return:
    """
    return jiwer.cer(r_list, h_list)
