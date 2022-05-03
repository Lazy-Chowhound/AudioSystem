import glob

from Dataset.Dataset import Dataset
from Util.AudioUtil import AUDIO_SETS_PATH, NOISE_AUDIO_SETS_PATH, get_audio_form


class AiShell(Dataset):
    def __init__(self, dataset):
        Dataset.__init__(self, dataset)
        self.dataset_path = AUDIO_SETS_PATH + dataset + "/"
        self.clips_path = AUDIO_SETS_PATH + dataset + "/wav/"
        self.noise_clips_path = NOISE_AUDIO_SETS_PATH + dataset + "/wav/"

    def get_name_and_pattern_tag(self, name):
        """
        从扰动名字中获取原本的名字和扰动标签
        :param name: 扰动音频名称，
        :return:
        """
        name = name.replace("\\", "/")
        return name[:name.find("_")] + ".wav", name[name.find("_") + 1:name.rfind(".")]

    def get_testset_audio_clips_list(self):
        """
        获取测试集
        :return:
        """
        testset_path = self.clips_path + "test/"
        audio_list = glob.glob(testset_path + "*/*.wav")
        audios = []
        for audio in audio_list:
            if get_audio_form(audio) == "wav":
                audios.append(audio.replace("\\", "/").replace(self.clips_path, ""))
        return audios

    def get_noise_testset_audio_clips_list(self):
        """
        获取扰动测试集
        :return:
        """
        noise_testset_path = self.noise_clips_path + "test/"
        audio_list = glob.glob(noise_testset_path + "*/*.wav")
        audios = []
        for audio in audio_list:
            if get_audio_form(audio) == "wav":
                audios.append(audio.replace("\\", "/").replace(self.noise_clips_path, ""))
        return audios
