import glob
import os

import librosa.display
import pandas as pd
import torch
from matplotlib import pyplot as plt
from pydub import AudioSegment
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

from Dataset.CommonVoice.CommonVoiceUtil import make_noise_audio_clips_dirs, write_noise_audio
from Dataset.Dataset import Dataset
from Perturbation.AudioProcess import *
from Util.AudioUtil import *
from Validation.Indicator import cer, cer_overall


class CommonVoice(Dataset):
    def __init__(self, dataset):
        Dataset.__init__(self, dataset)
        self.dataset_path = AUDIO_SETS_PATH + dataset + "/"
        self.clips_path = AUDIO_SETS_PATH + dataset + "/clips/"
        self.noise_clips_path = NOISE_AUDIO_SETS_PATH + dataset + "/clips/"
        self.model_dict = {"wav2vec2.0 Model": ["wav2vec2-large-xlsr-53-chinese-zh-cn"]}
        self.cer_dict = {"wav2vec2-large-xlsr-53-chinese-zh-cn": [0.1636319890171324, 0.43685204973427405]}

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
        audio_list = []
        for root, dirs, files in os.walk(self.clips_path):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    audio_list.append(file)
        return audio_list

    def get_audio_clip_content(self, audio_name):
        """
        获取指定数据集音频的详情
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :return:
        """
        files = ['validated.tsv', 'invalidated.tsv', 'other.tsv']
        for file in files:
            train = pd.read_csv(os.path.join(self.dataset_path, file), sep='\t', header=0)
            for index, row in train.iterrows():
                if audio_name in row['path']:
                    detail = dict(row.items())
                    return detail['sentence']

    def get_audio_clip_properties(self, audio_name):
        """
        获取某条音频所有属性
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :return:
        """
        audio_property = {}
        audio_property['name'] = audio_name
        audio_property['size'] = str(self.get_duration(audio_name)) + "秒"
        audio_property['channel'] = "单" if self.get_channels(audio_name) == 1 else "双"
        audio_property['sampleRate'] = str(self.get_sample_rate(audio_name)) + "Hz"
        audio_property['bitDepth'] = str(self.get_bit_depth(audio_name)) + "bit"
        audio_property['content'] = self.get_audio_clip_content(audio_name)
        return audio_property

    def get_sample_rate(self, audio):
        """
        获取音频的采样率
        :param audio: 音频名称，如common_voice_zh-CN_18524189.mp3
        :return:
        """
        samplingRate = librosa.get_samplerate(self.clips_path + audio)
        return samplingRate

    def get_duration(self, audio):
        """
        获取音频时长
        :param audio: 音频名称，如common_voice_zh-CN_18524189.mp3
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio, sr=None)
        return round(librosa.get_duration(sig, sr), 2)

    def get_channels(self, audio):
        """
        获取声道
        :param audio: 音频名称，如common_voice_zh-CN_18524189.mp3
        :return:
        """
        song = AudioSegment.from_mp3(self.clips_path + audio)
        return song.channels

    def get_bit_depth(self, audio):
        """
        获取位深
        :param audio: 音频名称，如common_voice_zh-CN_18524189.mp3
        :return:
        """
        song = AudioSegment.from_mp3(self.clips_path + audio)
        return song.sample_width * 8

    def get_waveform_graph(self, audio_name):
        """
        生成波形图
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
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
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :return:
        """
        audio = os.path.join(self.clips_path, audio_name)
        sig, sr = librosa.load(audio, sr=None)
        S = librosa.feature.melspectrogram(y=sig, sr=sr)
        plt.figure(figsize=(8, 5))
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                                 y_axis='mel', fmax=8000, x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel spectrogram')
        plt.tight_layout()
        savingPath = MEL_SPECTRUM_PATH + audio_name + ".jpg"
        plt.savefig(savingPath)
        return savingPath

    def get_noise_audio_clips_list(self):
        """
        获取扰动音频列表
        :return: [common_voice_zh-CN_18531538_gaussian_white_noise.mp3]
        """
        return os.listdir(self.noise_clips_path)

    def get_pattern_summary(self):
        """
        获取扰动大类的详情
        :return:
        """
        pattern_summary = {}
        for clip in self.get_noise_audio_clips_list():
            for key, value in pattern_to_name.items():
                if value in clip:
                    if key in pattern_summary.keys():
                        pattern_summary[key] = pattern_summary[key] + 1
                    else:
                        pattern_summary[key] = 1
                    break
        return pattern_summary

    def get_pattern_type_summary(self, pattern):
        """
        获取某个数据集某个扰动大类的具体扰动类型详情
        :param pattern: 扰动类别
        :return:
        """
        pattern_type_summary = {}
        name = pattern_to_name[pattern]
        for file in os.listdir(self.noise_clips_path):
            if name in file:
                if name == "gaussian_white_noise":
                    pattern_type = name
                else:
                    beg = file.index(name) + len(name) + 1
                    end = file.index(".")
                    pattern_type = file[beg:end]
                if pattern_type in pattern_type_summary.keys():
                    pattern_type_summary[pattern_type] = pattern_type_summary[pattern_type] + 1
                else:
                    pattern_type_summary[pattern_type] = 1
        return pattern_type_summary

    def get_audio_clips_pattern(self):
        """
        添加扰动时获取某数据集所有音频扰动情况
        :return:
        """
        audio_set_pattern = []
        key = 0
        for clip in self.get_noise_audio_clips_list():
            pattern_info = {"key": key}
            key += 1
            pattern_info["name"], pattern_tag = self.get_name_and_pattern_tag(clip)
            pattern_info["pattern"], pattern_info["patternType"] = get_pattern_info_from_pattern_tag(pattern_tag)
            audio_set_pattern.append(pattern_info)
        return audio_set_pattern

    def remove_current_noise_audio_clip(self, audio_name, pattern, pattern_type=None):
        """
        删除现有的扰动音频
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :param pattern: 扰动类别
        :param pattern_type: 具体扰动
        :return:
        """
        audio_name = add_tag(audio_name, pattern_to_name[pattern])
        if pattern_type is not None:
            audio_name = add_tag(audio_name, pattern_type_to_suffix(pattern_type))
        os.remove(self.noise_clips_path + audio_name)

    def add_gaussian_noise(self, audio_name):
        """
        添加高斯白噪声
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        noise_audio = sig + gaussian_white_noise(sig, snr=5)
        noise_wave_name = add_tag(audio_name, "gaussian_white_noise")
        make_noise_audio_clips_dirs(self.noise_clips_path + noise_wave_name)
        write_noise_audio(self.noise_clips_path, noise_wave_name, noise_audio, sr,
                          self.get_bit_depth(audio_name) / 8, self.get_channels(audio_name))

    def add_sound_level(self, audio_name, pattern_type):
        """
        添加 sound level 扰动
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :param pattern_type: 扰动类别
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
        noise_wave_name = add_tag(add_tag(audio_name, "sound_level"), pattern_type_to_suffix(pattern_type))
        make_noise_audio_clips_dirs(self.noise_clips_path + noise_wave_name)
        write_noise_audio(self.noise_clips_path, noise_wave_name, noise_audio, sr,
                          self.get_bit_depth(audio_name) / 8, self.get_channels(audio_name))

    def add_natural_sounds(self, audio_name, pattern_type):
        """
        添加 natural sound 扰动
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :param pattern_type: 扰动类别
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Natural sounds"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Natural Sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "natural_sounds"), pattern_type_to_suffix(pattern_type))
        make_noise_audio_clips_dirs(self.noise_clips_path + noise_wave_name)
        write_noise_audio(self.noise_clips_path, noise_wave_name, noise_audio, sr,
                          self.get_bit_depth(audio_name) / 8, self.get_channels(audio_name))

    def add_animal(self, audio_name, pattern_type):
        """
        添加 animal 扰动
        :param audio_name: 音频名称，如 common_voice_zh-CN_18524189.mp3
        :param pattern_type: 扰动类别
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Animal"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Animal", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "animal"),
                                  pattern_type_to_suffix(pattern_type))
        make_noise_audio_clips_dirs(self.noise_clips_path + noise_wave_name)
        write_noise_audio(self.noise_clips_path, noise_wave_name, noise_audio, sr,
                          self.get_bit_depth(audio_name) / 8, self.get_channels(audio_name))

    def add_sound_of_things(self, audio_name, pattern_type):
        """
        添加 sound of things 扰动
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :param pattern_type: 扰动类别
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Sound of things"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Sound of things", pattern_type), sr=sr,
                                               mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "sound_of_things"), pattern_type_to_suffix(pattern_type))
        make_noise_audio_clips_dirs(self.noise_clips_path + noise_wave_name)
        write_noise_audio(self.noise_clips_path, noise_wave_name, noise_audio, sr,
                          self.get_bit_depth(audio_name) / 8, self.get_channels(audio_name))

    def add_human_sounds(self, audio_name, pattern_type):
        """
        添加 human sounds 扰动
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :param pattern_type: 扰动类别
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Human sounds"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Human sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "human_sounds"), pattern_type_to_suffix(pattern_type))
        make_noise_audio_clips_dirs(self.noise_clips_path + noise_wave_name)
        write_noise_audio(self.noise_clips_path, noise_wave_name, noise_audio, sr,
                          self.get_bit_depth(audio_name) / 8, self.get_channels(audio_name))

    def add_music(self, audio_name, pattern_type):
        """
        添加 music 扰动
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :param pattern_type: 扰动类别
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Music"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Music", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "music"), pattern_type_to_suffix(pattern_type))
        make_noise_audio_clips_dirs(self.noise_clips_path + noise_wave_name)
        write_noise_audio(self.noise_clips_path, noise_wave_name, noise_audio, sr,
                          self.get_bit_depth(audio_name) / 8, self.get_channels(audio_name))

    def add_source_ambiguous_sounds(self, audio_name, pattern_type):
        """
        添加 source_ambiguous_sounds 扰动
       :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :param pattern_type: 扰动类别
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Source-ambiguous sounds"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Source-ambiguous sounds", pattern_type), sr=sr,
                                               mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_wave_name = add_tag(add_tag(audio_name, "source_ambiguous_sounds"), pattern_type_to_suffix(pattern_type))
        make_noise_audio_clips_dirs(self.noise_clips_path + noise_wave_name)
        write_noise_audio(self.noise_clips_path, noise_wave_name, noise_audio, sr,
                          self.get_bit_depth(audio_name) / 8, self.get_channels(audio_name))

    def get_name_and_pattern_tag(self, name):
        """
        从扰动名字中获取原本的名字和扰动标签
        :param name: 扰动音频名称，如common_voice_zh-CN_18524189_gaussian_white_noise.mp3
        :return: common_voice_zh-CN_18524189.mp3,gaussian_white_noise
        """
        num = re.findall("\\d+", name)[0]
        return name[0:name.find(num) + len(num)] + ".mp3", name[name.find(num) + len(num) + 1:name.find(".")]

    def get_num_of_clips_and_noise_clips(self):
        """
        获取原音频数量扰动音频的数量
        :return:
        """
        num_list = [len(self.get_audio_clips_list()), len(self.get_noise_audio_clips_list())]
        return num_list

    def get_testset_audio_clips_list(self):
        """
        获取测试集
        :return:
        """
        testTSV = self.dataset_path + "test.tsv"
        audios = []
        train = pd.read_csv(os.path.join(testTSV), sep='\t', header=0)
        for index, row in train.iterrows():
            detail = dict(row.items())
            audios.append(detail['path'])
        return audios

    def get_noise_testset_audio_clips_list(self):
        """
        获取测试集
        :return:
        """
        testset_path = self.noise_clips_path
        audio_list = glob.glob(testset_path + "*.mp3")
        audios = []
        for audio in audio_list:
            if get_audio_form(audio) == "mp3":
                audios.append(audio.replace("\\", "/").replace(self.noise_clips_path, ""))
        return audios

    def get_trainset_audio_clips_list(self):
        """
        获取训练集
        :return:
        """
        testTSV = self.dataset_path + "train.tsv"
        audios = []
        train = pd.read_csv(os.path.join(testTSV), sep='\t', header=0)
        for index, row in train.iterrows():
            detail = dict(row.items())
            audios.append(detail['path'])
        return audios

    def get_validation_results_by_page(self, model, page, page_size):
        """
        分页获取验证结果
        :param model: 模型名
        :param page: 页数
        :param page_size: 分页大小
        :return:
        """
        validation_results = []
        audio_list = self.get_testset_audio_clips_list()
        validation_results.append({"total": len(audio_list)})
        # 实时计算 由于时间太长这里就直接写死
        # pre_overall_cer, post_overall_cer = self.get_dataset_er()
        pre_overall_cer, post_overall_cer = round(self.cer_dict.get(model)[0], 3), round(self.cer_dict.get(model)[1], 3)
        validation_results.append({"preOverallER": pre_overall_cer})
        validation_results.append({"postOverallER": post_overall_cer})
        for index in range((int(page) - 1) * int(page_size), min(int(page) * int(page_size), len(audio_list))):
            audio_result = self.get_validation_result(audio_list[index], model)
            audio_result['key'] = index + 1
            validation_results.append(audio_result)
        return validation_results

    def get_validation_result(self, audio_name, model_name):
        """
        计算某一音频的所有验证内容
        :param audio_name: common_voice_zh-CN_18524189.mp3
        :param model_name: 模型名
        :return:
        """
        validation_result = {}
        validation_result['name'] = audio_name
        validation_result['realText'] = self.formalize(self.get_audio_clip_content(audio_name))
        validation_result['previousText'] = self.get_audio_clip_transcription(audio_name, model_name)
        validation_result['preER'] = round(cer(validation_result['realText'], validation_result['previousText']), 2)
        noise_audio_name = self.get_noise_clip_name(audio_name)
        validation_result['noise_audio_name'] = noise_audio_name
        validation_result['posteriorText'] = self.get_noise_audio_clip_transcription(noise_audio_name, model_name)
        validation_result['postER'] = round(cer(validation_result['realText'], validation_result['posteriorText']), 2)
        return validation_result

    def get_audio_clip_transcription(self, audio_name, model_name):
        """
        获取原音频识别出的内容
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189.mp3
        :param model_name: 模型名
        :return:
        """
        audio, rate = librosa.load(self.clips_path + audio_name, sr=16000)
        if model_name in self.model_dict.get("wav2vec2.0 Model"):
            inputs = self.processor(audio, sampling_rate=rate, return_tensors="pt", padding=True)
            with torch.no_grad():
                logits = self.model(inputs.input_values, attention_mask=inputs.attention_mask).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            predicted_sentences = self.processor.batch_decode(predicted_ids)
            return self.formalize(predicted_sentences[0])

    def get_noise_audio_clip_transcription(self, audio_name, model_name):
        """
        获取扰动音频识别出的内容
        :param audio_name: 扰动音频名称，如common_voice_zh-CN_18524189_sound_level_pitch.mp3
        :param model_name: 模型名
        :return:
        """
        audio, rate = librosa.load(self.noise_clips_path + audio_name, sr=16000)
        if model_name in self.model_dict.get("wav2vec2.0 Model"):
            inputs = self.processor(audio, sampling_rate=rate, return_tensors="pt", padding=True)
            with torch.no_grad():
                logits = self.model(inputs.input_values, attention_mask=inputs.attention_mask).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            predicted_sentences = self.processor.batch_decode(predicted_ids)
            return self.formalize(predicted_sentences[0])

    def get_dataset_er(self, model_name):
        """
        获取数据集总体上的 WER/CER
        :param model_name: 模型名
        :return:
        """
        if len(self.real_text_list) == 0 or len(self.previous_text_list) == 0 or len(self.post_text_list) == 0:
            self.get_dataset_texts(model_name)
        return cer_overall(self.real_text_list, self.previous_text_list), cer_overall(self.real_text_list,
                                                                                      self.post_text_list)

    def get_dataset_texts(self, model_name):
        """
        获取训练集上所欲音频的前后文本
        :param model_name: 模型名
        :return:
        """
        audio_list = self.get_testset_audio_clips_list()
        for audio in audio_list:
            self.real_text_list.append(self.get_audio_clip_content(audio))
            self.previous_text_list.append(self.get_audio_clip_transcription(audio, model_name))
            noise_audio = self.get_noise_clip_name(audio)
            self.post_text_list.append(self.get_noise_audio_clip_transcription(noise_audio, model_name))

    def load_model(self, model_name):
        """
        加载模型
        :param model_name: 模型名
        :return:
        """
        if not os.path.exists(self.model_path + model_name):
            return False
        if self.model is None or self.processor is None:
            if model_name in self.model_dict.get("wav2vec2.0 Model"):
                self.processor = Wav2Vec2Processor.from_pretrained(self.model_path + model_name)
                self.model = Wav2Vec2ForCTC.from_pretrained(self.model_path + model_name)
        return True

    def get_noise_clip_name(self, audio_name):
        """
        获取原音频对应的扰动音频名称
        :param audio_name: 音频名称，如common_voice_zh-CN_18524189_sound_level_pitch.mp3
        :return:
        """
        for file in os.listdir(self.noise_clips_path):
            if file.startswith(audio_name[0:audio_name.find(".")]):
                return file

    def judge_model(self, model):
        """
        判断模型适不适用于该数据集
        :param model: 模型名
        :return:
        """
        for (key, value) in self.model_dict.items():
            if model in value:
                return True
        return False

    def formalize(self, sentence):
        """
        规范化文本
        :param sentence: 识别出的内容
        :return:
        """
        CHARS_TO_IGNORE = [",", "?", "¿", ".", "!", "¡", ";", "；", ":", '""', "%", '"', "�", "ʿ", "·", "჻", "~",
                           "՞", "؟", "،", "।", "॥", "«", "»", "„", "“", "”", "「", "」", "‘", "’", "《", "》", "(", ")",
                           "[", "]", "{", "}", "=", "`", "_", "+", "<", ">", "…", "–", "°", "´", "ʾ", "‹", "›", "©",
                           "®", "—", "→", "。", "、", "﹂", "﹁", "‧", "～", "﹏", "，", "｛", "｝", "（", "）", "［", "］",
                           "【", "】", "‥", "〽", "『", "』", "〝", "〟", "⟨", "⟩", "〜", "：", "！", "？", "♪", "؛", "/", "\\",
                           "º", "−", "^", "'", "ʻ", "ˆ", "<unk>"]
        chars_to_ignore_regex = f"[{re.escape(''.join(CHARS_TO_IGNORE))}]"
        return re.sub(chars_to_ignore_regex, "", sentence)
