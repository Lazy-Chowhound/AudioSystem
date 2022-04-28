import math
import subprocess


def split_text(path="D:\AudioSystem\Audio\jtubespeech\word\word\ja\jawiki-latest-pages-articles-multistream-index.txt",
               num=500):
    with open(path, 'r', encoding="utf-8") as f:
        words = f.read().splitlines()
    word_slice = math.ceil(len(words) / num)
    for i in range(0, num):
        start = i * word_slice
        end = min(len(words), (i + 1) * word_slice)
        with open("D:\AudioSystem\Audio\jtubespeech\word\word\ja/" + str(i) + ".txt", "a", encoding="utf-8") as f:
            for word in words[start:end]:
                f.writelines(word + "\n")


def run_cmd_Popen_PIPE(cmd_string):
    """
    执行cmd命令，并得到执行后的返回值,python调试界面不输出返回值
    :param cmd_string: cmd命令，如：'adb devices"'
    :return:
    """
    print('运行cmd指令：{}'.format(cmd_string))
    return subprocess.Popen(cmd_string, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8").communicate()[0]


if __name__ == '__main__':
    dpath = "D:/AudioSystem/Audio/jtubespeech/"
    script_path = dpath + "scripts/obtain_video_id.py"
    word_path = dpath + "word/word/ja/{num}.txt"
    output_path = dpath + "videoid"
    cmd = ("python " + script_path + " ja " + word_path + " --outdir " + output_path).format(num=0)
    run_cmd_Popen_PIPE(cmd)
