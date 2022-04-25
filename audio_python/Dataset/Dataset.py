import librosa
import soundfile

from Dataset.DatasetUtil import make_dirs
from Perturbation.AudioProcess import gaussian_white_noise, louder, quieter, change_pitch, add_noise
from Util.AudioUtil import MODEL_PATH, add_tag, pattern_type_to_suffix, get_source_noises_path, pattern_types_dict


class Dataset:
    def __init__(self, dataset):
        self.dataset = dataset
        self.model = None
        self.processor = None
        self.model_path = MODEL_PATH
        self.real_text_list = []
        self.previous_text_list = []
        self.post_text_list = []
        self.clips_path = ""
        self.noise_clips_path = ""

    def get_audio_clips_properties_by_page(self, page, page_size):
        """
        分页获取音频及其属性
        :param page: 页数
        :param page_size: 页面大小
        """
        pass

    def get_audio_clips_list(self):
        """
        获取目录下所有音频文件名
        """
        pass

    def get_audio_clip_content(self, audio_name):
        """
        获取指定数据集音频的详情
        :param audio_name: 音频名称
        """
        pass

    def get_audio_clip_properties(self, audio_name):
        """
        获取某条音频所有属性
        :param audio_name:音频名称
        """
        audio_property = {}
        return audio_property

    def get_sample_rate(self, audio):
        """
        获取音频的采样率
        :param audio: 音频绝对路径
        """
        pass

    def get_duration(self, audio):
        """
        获取音频时长
        :param audio: 音频绝对路径
        """
        pass

    def get_channels(self, audio):
        """
        获取声道
        :param audio: 音频绝对路径
        """
        pass

    def get_bit_depth(self, audio):
        """
        获取位深
        :param audio: 音频绝对路径
        """
        pass

    def get_waveform_graph(self, audio_name):
        """
        生成波形图
        :param audio_name: 音频名称
        """
        pass

    def get_mel_spectrum(self, audio_name):
        """
        生成 Mel频谱图
        :param audio_name: 音频名称
        :return:
        """
        pass

    def get_noise_audio_clips_list(self):
        """
        获取扰动音频列表
        """
        pass

    def get_pattern_summary(self):
        """
        获取扰动大类的详情
        """
        pattern_summary = {}
        return pattern_summary

    def get_pattern_type_summary(self, pattern):
        """
        获取某个数据集某个扰动大类的具体扰动类型详情
        :param pattern: Sound level
        """
        pattern_type_summary = {}
        return pattern_type_summary

    def get_audio_clips_pattern(self):
        """
        添加扰动时获取某数据集所有音频扰动情况
        :return:
        """
        audio_set_pattern = []
        return audio_set_pattern

    def remove_current_noise_audio_clip(self, audio_name, pattern, pattern_type=None):
        """
        删除现有的扰动音频
        :param audio_name: 音频名
        :param pattern: Animal
        :param pattern_type: Wild animals
        :return:
        """
        pass

    def add_gaussian_noise(self, audio_name):
        """
        添加高斯白噪声
        :param audio_name:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        noise_audio = sig + gaussian_white_noise(sig, snr=5)
        noise_audio_name = add_tag(audio_name, "gaussian_white_noise")
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)

    def add_sound_level(self, audio_name, pattern_type):
        """
        添加 sound level 扰动
        :param audio_name:
        :param pattern_type: 具体扰动
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        noise_audio = sig
        if pattern_type == "Louder":
            noise_audio = louder(sig)
        elif pattern_type == "Quieter":
            noise_audio = quieter(sig)
        elif pattern_type == "Pitch":
            noise_audio = change_pitch(sig, sr)
        elif pattern_type == "Speed":
            sr = sr * 2
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "sound_level"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_natural_sounds(self, audio_name, pattern_type):
        """
        添加 natural sound 扰动
        :param audio_name:
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Natural sounds"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Natural Sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "natural_sounds"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_animal(self, audio_name, pattern_type):
        """
        添加 animal 扰动
        :param audio_name:
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Animal"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Animal", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "animal"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_sound_of_things(self, audio_name, pattern_type):
        """
        添加 sound of things 扰动
        :param audio_name:
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Sound of things"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Sound of things", pattern_type), sr=sr,
                                               mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "sound_of_things"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_human_sounds(self, audio_name, pattern_type):
        """
        添加 human sounds 扰动
        :param audio_name:
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Human sounds"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Human sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "human_sounds"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_music(self, audio_name, pattern_type):
        """
        添加 music 扰动
        :param audio_name:
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Music"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Music", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "music"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_source_ambiguous_sounds(self, audio_name, pattern_type):
        """
        添加 source_ambiguous_sounds 扰动
        :param audio_name:
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Source-ambiguous sounds"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Source-ambiguous sounds", pattern_type), sr=sr,
                                               mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "source_ambiguous_sounds"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def get_name_and_pattern_tag(self, name):
        """
        从扰动名字中获取原本的名字和扰动标签
        :param name: 扰动音频名
        """
        pass

    def get_testset_audio_clips_list(self):
        """
        获取测试集
        :return:
        """
        audios = []
        return audios

    def get_validation_results_by_page(self, model, page, page_size):
        """
        分页获取验证结果
        :param model: 模型名
        :param page: 页数
        :param page_size: 分页大小
        """
        validation_results = []
        return validation_results

    def get_validation_result(self, audio_name, model_name):
        """
        计算某一音频的所有验证内容
        :param audio_name: 音频名
        :param model_name: 模型名
        """
        validation_result = {}
        return validation_result

    def get_audio_clip_transcription(self, audio_name, model_name):
        """
        获取原音频识别出的内容
        :param audio_name: 音频名
        :param model_name: 模型名
        """
        pass

    def get_noise_audio_clip_transcription(self, audio_name, model_name):
        """
        获取扰动音频识别出的内容
        :param audio_name: 音频名
        :param model_name: 模型名
        """
        pass

    def get_dataset_er(self, model_name):
        """
        获取数据集总体上的 WER/CER
        :param model_name: 模型名
        """
        pass

    def get_dataset_texts(self, model_name):
        """
        :param model_name: 模型名
        :return:
        """
        pass

    def load_model(self, model_name):
        """
        加载模型
        :param model_name: 模型名
        """
        pass

    def get_noise_clip_name(self, audio_name):
        """
        获取原音频对应的扰动音频名称
        :param audio_name: 音频名
        """
        pass

    def judge_model(self, model):
        """
        判断模型适不适用于该数据集
        :param model:模型名
        :return:
        """
        pass

    def formalize(self, sentence):
        """
        规范化句子
        :param sentence:
        """
        pass
