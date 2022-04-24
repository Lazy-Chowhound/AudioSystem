import os
import tarfile


def unzip_tgz(path):
    """
    解压 tar.gz 文件
    :param path:
    :return:
    """
    tgz_lists = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.gz':
                tgz_lists.append(os.path.join(path, file))
    for file in tgz_lists:
        tf = tarfile.open(file)
        tf.extractall(path)
        print(file + "已被解压")


def make_dirs(path):
    """
    根据文件路径，生成所需文件夹
    :param path:
    :return:
    """
    target_dir = path[0:path.rfind("/")]
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


if __name__ == '__main__':
    unzip_tgz("D:/AudioSystem/Audio/data_aishell/wav/")
