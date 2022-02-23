import glob

import librosa.display
import numpy as np
import soundfile
from matplotlib import pyplot as plt
from pydub import AudioSegment

from Dataset.TimitDataset.TimitDatasetAudioUtil import make_noise_audio_clips_dirs
from Perturbation.AudioProcess import gaussian_white_noise, louder, quieter, change_pitch, add_noise
from Util.AudioUtil import *


class TimitDataset:
    def __init__(self, dataset):
        self.dataset = dataset
        self.dataset_path = AUDIO_SETS_PATH + dataset + "/"
        self.clips_path = AUDIO_SETS_PATH + dataset + "/lisa/data/timit/raw/TIMIT/TRAIN/"
        self.noise_clips_path = NOISE_AUDIO_SETS_PATH + dataset + "/lisa/data/timit/raw/TIMIT/TRAIN/"

    def get_audio_clips_properties_by_page(self, page, page_size):
        """
        分页获取音频及其属性
        :param page: 页数
        :param page_size: 页面大小
        :return:
        """
        audio = []
        audio_clips_list = self.get_audio_clips_list()
        audio.append({'total': len(audio_clips_list)})
        for i in range((int(page) - 1) * int(page_size), min(int(page) * int(page_size), len(audio_clips_list))):
            audio_property = self.get_audio_clip_properties(audio_clips_list[i])
            audio_property['key'] = i + 1
            audio.append(audio_property)
        return audio

    def get_audio_clips_list(self):
        """
        获取目录下所有音频文件名
        :return:[DR1/FCJF0/SA1_n.wav]
        """
        audioList = glob.glob(self.clips_path + "*/*/*.wav")
        audios = []
        for audio in audioList:
            if getAudioForm(audio) == "wav":
                audios.append(audio.replace("\\", "/").replace(self.clips_path, ""))
        return audios

    def get_audio_clip_detail(self, audio_name):
        """
        获取指定数据集音频的详情
        :param audio_name: DR1/FCJF0/SA1_n.wav
        :return:
        """
        txtPath = self.clips_path + audio_name.replace("_n.wav", ".TXT")
        with open(txtPath, "r") as f:
            line = f.readline()
            content = line.split(" ")[2:]
        return " ".join(content).replace("\n", "")

    def get_audio_clip_properties(self, audio_name):
        """
        获取某条音频所有属性
        :param audio_name:DR1/FCJF0/SA1_n.wav
        :return:
        """
        audio = self.clips_path + audio_name
        audio_property = {}
        audio_property['name'] = audio_name
        audio_property['size'] = str(self.get_duration(audio)) + "秒"
        audio_property['channel'] = "单" if self.get_channels(audio) == 1 else "双"
        audio_property['sampleRate'] = str(self.getSamplingRate(audio)) + "Hz"
        audio_property['bitDepth'] = str(self.get_bit_depth(audio)) + "bit"
        audio_property['content'] = self.get_audio_clip_detail(audio_name)
        return audio_property

    def getSamplingRate(self, audio):
        """
        获取音频的采样率
        :param audio: 音频绝对路径
        :return:
        """
        samplingRate = librosa.get_samplerate(audio)
        return samplingRate

    def get_duration(self, audio):
        """
        获取音频时长
        :param audio: 音频绝对路径
        :return:
        """
        sig, sr = librosa.load(audio, sr=None)
        return round(librosa.get_duration(sig, sr), 2)

    def get_channels(self, audio):
        """
        获取声道
        :param audio: 音频绝对路径
        :return:
        """
        song = AudioSegment.from_wav(audio)
        return song.channels

    def get_bit_depth(self, audio):
        """
        获取位深
        :param audio: 音频绝对路径
        :return:
        """
        song = AudioSegment.from_wav(audio)
        return song.sample_width * 8

    def get_waveform_graph(self, audio_name):
        """
        生成波形图
        :param audio_name: DR1/FCJF0/SA1_n.wav
        :return:
        """
        audio = os.path.join(self.clips_path, audio_name)
        sig, sr = librosa.load(audio, sr=None)
        plt.figure(figsize=(8, 5))
        librosa.display.waveshow(sig, sr=sr)
        plt.ylabel('Amplitude')
        savingPath = WAVEFORM_GRAPH_PATH + audio_name + ".jpg"
        if not os.path.exists(savingPath[0:savingPath.rfind("/")]):
            os.makedirs(savingPath[0:savingPath.rfind("/")])
        plt.savefig(savingPath)
        return savingPath

    def get_mel_spectrum(self, audio_name):
        """
        生成 Mel频谱图
        :param audio_name: DR1/FCJF0/SA1_n.wav
        :return:
        """
        audio = os.path.join(self.clips_path, audio_name)
        sig, sr = librosa.load(audio, sr=None)
        S = librosa.feature.melspectrogram(y=sig, sr=sr)
        plt.figure(figsize=(8, 5))
        librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
                                 y_axis='mel', fmax=8000, x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel spectrogram')
        plt.tight_layout()
        savingPath = MEL_SPECTRUM_PATH + audio_name + ".jpg"
        if not os.path.exists(savingPath[0:savingPath.rfind("/")]):
            os.makedirs(savingPath[0:savingPath.rfind("/")])
        plt.savefig(savingPath)
        return savingPath

    def get_pattern_summary(self):
        """
        获取扰动大类的详情
        :return:
        """
        summary = {}
        noise_clips = glob.glob(self.noise_clips_path + "*/*/*.wav")
        for file in noise_clips:
            for key, value in pattern_to_name.items():
                if value in file:
                    if key in summary.keys():
                        summary[key] = summary[key] + 1
                    else:
                        summary[key] = 1
                    break
        sorted(summary)
        return summary

    def get_pattern_detail(self, pattern):
        """
        获取某个数据集某个扰动大类的具体扰动类型详情
        :param pattern: Sound level
        :return:
        """
        summaryDetail = {}
        name = pattern_to_name[pattern]
        noise_clips = glob.glob(self.noise_clips_path + "*/*/*.wav")
        for file in noise_clips:
            if name in file:
                if name == "gaussian_white_noise":
                    pattern = name
                else:
                    beg = file.index(name) + len(name) + 1
                    end = file.index(".")
                    pattern = file[beg:end]
                if pattern in summaryDetail.keys():
                    summaryDetail[pattern] = summaryDetail[pattern] + 1
                else:
                    summaryDetail[pattern] = 1
        sorted(summaryDetail)
        return summaryDetail

    def get_audio_clips_pattern(self):
        """
        添加扰动时获取某数据集所有音频扰动情况
        :return:
        """
        audio_set_pattern = []
        key = 0
        noise_clips = glob.glob(self.noise_clips_path + "*/*/*.wav")
        for file in noise_clips:
            pattern_info = {"key": key}
            key += 1
            file = file.replace("\\", "/")
            noise_audio_name = file[file.rfind("/") + 1:]
            pattern_info["name"] = noise_audio_name[0:noise_audio_name.find("_n") + 2]
            pattern_tag = noise_audio_name[noise_audio_name.find("_n") + 3:noise_audio_name.find(".")]
            pattern_info["pattern"], pattern_info["patternType"] = get_pattern_info_from_name(pattern_tag)
            audio_set_pattern.append(pattern_info)
        return audio_set_pattern

    def remove_current_noise_audio_clip(self, audio_name, pattern, pattern_type=None):
        """
        删除现有的扰动音频
        :param audio_name: DR1/FCJF0/SA1_n.wav
        :param pattern: Animal
        :param pattern_type: Wild animals
        :return:
        """
        audio_name = add_tag(audio_name, pattern_to_name[pattern])
        if pattern_type is not None:
            audio_name = add_tag(audio_name, pattern_type_to_suffix(pattern_type))
        remove_audio(self.noise_clips_path, audio_name)

    def add_gaussian_noise(self, audio_name):
        """
        添加高斯白噪声
        :param audio_name: DR1/FCJF0/SA1_n.wav
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        noise_audio = gaussian_white_noise(sig, snr=5)
        noise_audio_name = add_tag(audio_name, "gaussian_white_noise")
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_noise_audio_clips_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)

    def add_sound_level(self, audio_name, pattern_type):
        """
        添加 sound level 扰动
        :param audio_name: DR1/FCJF0/SA1_n.wav
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
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_natural_sounds(self, audio_name, pattern_type):
        """
        添加 natural sound 扰动
        :param audio_name: DR1/FCJF0/SA1_n.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in natural_sounds_pattern_types:
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Natural Sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "natural_sounds"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_animal(self, audio_name, pattern_type):
        """
        添加 animal 扰动
        :param audio_name: DR1/FCJF0/SA1_n.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in animal_pattern_types:
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Animal", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "animal"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_sound_of_things(self, audio_name, pattern_type):
        """
        添加 sound of things 扰动
        :param audio_name: DR1/FCJF0/SA1_n.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in sound_of_things_pattern_types:
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Sound of things", pattern_type), sr=sr,
                                               mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "sound_of_things"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_human_sounds(self, audio_name, pattern_type):
        """
        添加 human sounds 扰动
        :param audio_name: 形如 DR1/FCJF0/SA1_n.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in human_sounds_pattern_types:
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Human sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "human_sounds"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_music(self, audio_name, pattern_type):
        """
        添加 music 扰动
        :param audio_name: 形如 DR1/FCJF0/SA1_n.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in music_pattern_types:
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Music", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "music"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_source_ambiguous_sounds(self, audio_name, pattern_type):
        """
        添加 source_ambiguous_sounds 扰动
        :param audio_name: DR1/FCJF0/SA1_n.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in source_ambiguous_sounds_pattern_types:
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Source-ambiguous sounds", pattern_type), sr=sr,
                                               mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "source_ambiguous_sounds"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""


if __name__ == '__main__':
    pass
