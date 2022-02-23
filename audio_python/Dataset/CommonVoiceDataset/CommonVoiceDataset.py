import librosa.display
import pandas as pd
from matplotlib import pyplot as plt
from pydub import AudioSegment

from Dataset.CommonVoiceDataset.CommonVoiceDatasetAudioUtil import write_noise_audio
from Perturbation.AudioProcess import *
from Util.AudioUtil import *


class CommonVoiceDataset:
    def __init__(self, dataset):
        self.dataset = dataset
        self.dataset_path = AUDIO_SETS_PATH + dataset + "/"
        self.clips_path = AUDIO_SETS_PATH + dataset + "/clips/"
        self.noise_clips_path = NOISE_AUDIO_SETS_PATH + dataset + "/clips/"

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
        :return:
        """
        audioList = []
        for root, dirs, files in os.walk(self.clips_path):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    audioList.append(file)
        return audioList

    def get_audio_clip_detail(self, audio_name):
        """
        获取指定数据集音频的详情
        :param audio_name:
        :return:
        """
        files = ['validated.tsv', 'invalidated.tsv', 'other.tsv']
        detail = {}
        for file in files:
            train = pd.read_csv(os.path.join(self.dataset_path, file), sep='\t', header=0)
            for index, row in train.iterrows():
                if audio_name in row['path']:
                    detail = dict(row.items())
                    detail['id'] = index
                    break
        return detail

    def get_audio_clip_properties(self, audio_name):
        """
        获取某条音频所有属性
        :return:
        """
        audio = self.clips_path + audio_name
        audio_property = {}
        detail = self.get_audio_clip_detail(audio_name)
        audio_property['name'] = audio_name
        audio_property['size'] = str(self.get_duration(audio)) + "秒"
        audio_property['channel'] = "单" if self.get_channels(audio) == 1 else "双"
        audio_property['sampleRate'] = str(self.getSamplingRate(audio)) + "Hz"
        audio_property['bitDepth'] = str(self.get_bit_depth(audio)) + "bit"
        audio_property['content'] = detail['sentence']
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
        song = AudioSegment.from_mp3(audio)
        return song.channels

    def get_bit_depth(self, audio):
        """
        获取位深
        :param audio: 音频绝对路径
        :return:
        """
        song = AudioSegment.from_mp3(audio)
        return song.sample_width * 8

    def get_waveform_graph(self, audio_name):
        """
        生成波形图
        :param audio_name: 音频名
        :return:
        """
        audio = os.path.join(self.clips_path, audio_name)
        sig, sr = librosa.load(audio, sr=None)
        plt.figure(figsize=(8, 5))
        librosa.display.waveshow(sig, sr=sr)
        plt.ylabel('Amplitude')
        savingPath = WAVEFORM_GRAPH_PATH + audio_name + ".jpg"
        plt.savefig(savingPath)
        return savingPath

    def get_mel_spectrum(self, audio_name):
        """
        生成 Mel频谱图
        :param audio_name: 音频名
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
        plt.savefig(savingPath)
        return savingPath

    def get_pattern_summary(self):
        """
        获取扰动大类的详情
        :return:
        """
        summary = {}
        for file in os.listdir(self.noise_clips_path):
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
        for file in os.listdir(self.noise_clips_path):
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
        for root, dirs, files in os.walk(self.noise_clips_path):
            for file in files:
                pattern_info = {"key": key}
                key += 1
                num = re.findall("\\d+", file)[0]
                pattern_info["name"] = file[0:file.find(num) + len(num)] + ".mp3"
                pattern_tag = file[file.find(num) + len(num) + 1:file.find(".")]
                pattern_info["pattern"], pattern_info["patternType"] = get_pattern_info_from_name(pattern_tag)
                audio_set_pattern.append(pattern_info)
        return audio_set_pattern

    def remove_current_noise_audio_clip(self, audio_name, pattern, pattern_type=None):
        """
        删除现有的扰动音频
        :param audio_name: common_voice_zh-CN_18524189.mp3
        :param pattern: Animal
        :param pattern_type: Wild animals
        :return:
        """
        path = self.noise_clips_path
        audio_name = add_tag(audio_name, pattern_to_name[pattern])
        if pattern_type is not None:
            audio_name = add_tag(audio_name, pattern_type_to_suffix(pattern_type))
        remove_audio(path, audio_name)

    def add_gaussian_noise(self, audio_name):
        """
        添加高斯白噪声
        :param audio_name: common_voice_zh-CN_18524189.mp3
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        noise_audio = gaussian_white_noise(sig, snr=5)
        wave_path = self.noise_clips_path
        wave_name = audio_name.replace(".mp3", ".wav")
        noise_wave_name = add_tag(wave_name, "gaussian_white_noise")
        write_noise_audio(wave_path, noise_wave_name, noise_audio, sr)

    def add_sound_level(self, audio_name, pattern_type):
        """
        添加 sound level 扰动
        :param audio_name: common_voice_zh-CN_18524189.mp3
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        noise_audio = sig
        wave_path = self.noise_clips_path
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
        noise_wave_name = add_tag(add_tag(audio_name, "sound_level"),
                                  pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
        write_noise_audio(wave_path, noise_wave_name, noise_audio, sr)
        return ""

    def add_natural_sounds(self, audio_name, pattern_type):
        """
        添加 natural sound 扰动
        :param audio_name: common_voice_zh-CN_18524189.mp3
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        wave_path = self.noise_clips_path
        if pattern_type in natural_sounds_pattern_types:
            noiseSig, noise_sr = librosa.load(get_source_noises_path("Natural Sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noiseSig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "natural_sounds"),
                                  pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
        write_noise_audio(wave_path, noise_wave_name, noise_audio, sr)
        return ""

    def add_animal(self, audio_name, pattern_type):
        """
        添加 animal 扰动
        :param audio_name: common_voice_zh-CN_18524189.mp3
        :param pattern_type:
        :return:
        """
        path = self.clips_path
        sig, sr = librosa.load(path + audio_name, sr=None)
        wave_path = self.noise_clips_path
        if pattern_type in animal_pattern_types:
            noiseSig, noise_sr = librosa.load(get_source_noises_path("Animal", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noiseSig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "animal"),
                                  pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
        write_noise_audio(wave_path, noise_wave_name, noise_audio, sr)
        return ""

    def add_sound_of_things(self, audio_name, pattern_type):
        """
        添加 sound of things 扰动
        :param audio_name: common_voice_zh-CN_18524189.mp3
        :param pattern_type:
        :return:
        """
        path = self.clips_path
        sig, sr = librosa.load(path + audio_name, sr=None)
        wave_path = self.noise_clips_path
        if pattern_type in sound_of_things_pattern_types:
            noiseSig, noise_sr = librosa.load(get_source_noises_path("Sound of things", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noiseSig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "sound_of_things"),
                                  pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
        write_noise_audio(wave_path, noise_wave_name, noise_audio, sr)
        return ""

    def add_human_sounds(self, audio_name, pattern_type):
        """
        添加 human sounds 扰动
        :param audio_name: 形如 common_voice_zh-CN_18524189.mp3
        :param pattern_type:
        :return:
        """
        path = self.clips_path
        sig, sr = librosa.load(path + audio_name, sr=None)
        wave_path = self.noise_clips_path
        if pattern_type in human_sounds_pattern_types:
            noiseSig, noise_sr = librosa.load(get_source_noises_path("Human sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noiseSig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "human_sounds"),
                                  pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
        write_noise_audio(wave_path, noise_wave_name, noise_audio, sr)
        return ""

    def add_music(self, audio_name, pattern_type):
        """
        添加 music 扰动
        :param audio_name: 形如 common_voice_zh-CN_18524189.mp3
        :param pattern_type:
        :return:
        """
        path = self.clips_path
        sig, sr = librosa.load(path + audio_name, sr=None)
        wave_path = self.noise_clips_path
        if pattern_type in music_pattern_types:
            noiseSig, noise_sr = librosa.load(get_source_noises_path("Music", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noiseSig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "music"),
                                  pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
        write_noise_audio(wave_path, noise_wave_name, noise_audio, sr)
        return ""

    def add_source_ambiguous_sounds(self, audio_name, pattern_type):
        """
        添加 source_ambiguous_sounds 扰动
        :param audio_name: common_voice_zh-CN_18524189.mp3
        :param pattern_type:
        :return:
        """
        path = self.clips_path
        sig, sr = librosa.load(path + audio_name, sr=None)
        wave_path = self.noise_clips_path
        if pattern_type in source_ambiguous_sounds_pattern_types:
            noiseSig, noise_sr = librosa.load(get_source_noises_path("Source-ambiguous sounds", pattern_type), sr=sr,
                                              mono=True)
            noise_audio = add_noise(sig, noiseSig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "source_ambiguous_sounds"),
                                  pattern_type_to_suffix(pattern_type)).replace(".mp3", ".wav")
        write_noise_audio(wave_path, noise_wave_name, noise_audio, sr)
        return ""
