import os


def make_dirs(path):
    """
    根据文件路径，生成所需文件夹
    :param path:
    :return:
    """
    target_dir = path[0:path.rfind("/")]
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
