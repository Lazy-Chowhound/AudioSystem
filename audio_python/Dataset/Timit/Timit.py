import glob
import os

import librosa.display
import numpy as np
import torch
from matplotlib import pyplot as plt
from pydub import AudioSegment
from transformers import AutoProcessor, AutoModelForCTC, AutoModelForSpeechSeq2Seq, Wav2Vec2Processor, HubertForCTC, \
    Data2VecAudioForCTC

from Dataset.Dataset import Dataset
from Util.AudioUtil import *
from Validation.Indicator import wer, wer_overall


class Timit(Dataset):
    def __init__(self, dataset):
        Dataset.__init__(self, dataset)
        self.dataset_path = AUDIO_SETS_PATH + dataset + "/"
        self.clips_path = AUDIO_SETS_PATH + dataset + "/lisa/data/timit/raw/TIMIT/"
        self.noise_clips_path = NOISE_AUDIO_SETS_PATH + dataset + "/lisa/data/timit/raw/TIMIT/"
        self.model_dict = {
            "wav2vec2.0 Model": ["wav2vec2-large-960h", "wav2vec2-large-lv60-timit-asr", "wav2vec2-base-timit-asr"],
            "S2T Model": ["s2t-small-librispeech-asr", "s2t-medium-librispeech-asr", "s2t-large-librispeech-asr"],
            "HuBert Model": ["hubert-large-ls960-ft"],
            "Data2Vec Model": ["data2vec-audio-base-960h"],
            "UniSpeech Model": ["unispeech-large-1500h-cv-timit0", "unispeech-large-1500h-cv-timit1",
                                "unispeech-large-1500h-cv-timit2", "unispeech-large-1500h-cv-timit3"]}
        self.wer_dict = {"wav2vec2-large-960h": [0.09985528219971057, 0.23664806009234374],
                         "wav2vec2-large-lv60-timit-asr": [0.1386534353249259, 0],
                         "wav2vec2-base-timit-asr": [0.2555992006064365, 0],
                         "s2t-small-librispeech-asr": [0.10778030459651299, 0],
                         "s2t-medium-librispeech-asr": [0.11412032251395493, 0],
                         "s2t-large-librispeech-asr": [0.10281855144373234, 0.2819929708497002],
                         "hubert-large-ls960-ft": [0.06594996898904279, 0.15174695058920817],
                         "data2vec-audio-base-960h": [0.08765763903245813, 0.26951967472951555],
                         "unispeech-large-1500h-cv-timit": [0.23816415133347116, 0.4294673006684584]}

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
        :return:[TRAIN/DR1/FCJF0/SA1_n.wav]
        """
        audio_list = glob.glob(self.clips_path + "*/*/*/*.wav")
        audios = []
        for audio in audio_list:
            if get_audio_form(audio) == "wav":
                audios.append(audio.replace("\\", "/").replace(self.clips_path, ""))
        return audios

    def get_audio_clip_content(self, audio_name):
        """
        获取指定数据集音频的详情
        :param audio_name: 音频名称，如 TRAIN/DR1/FCJF0/SA1_n.wav
        :return:
        """
        txtPath = self.clips_path + audio_name.replace("_n.wav", ".TXT")
        with open(txtPath, "r") as f:
            line = f.readline()
            content = line.split(" ")[2:]
            content = " ".join(content).replace("\n", "")
        return content[0:len(content) - 1]

    def get_audio_clip_properties(self, audio_name):
        """
        获取某条音频所有属性
        :param audio_name: 音频名称，如 TRAIN/DR1/FCJF0/SA1_n.wav
        :return:
        """
        audio = self.clips_path + audio_name
        audio_property = {}
        audio_property['name'] = audio_name
        audio_property['size'] = str(self.get_duration(audio)) + "秒"
        audio_property['channel'] = "单" if self.get_channels(audio) == 1 else "双"
        audio_property['sampleRate'] = str(self.get_sample_rate(audio)) + "Hz"
        audio_property['bitDepth'] = str(self.get_bit_depth(audio)) + "bit"
        audio_property['content'] = self.get_audio_clip_content(audio_name)
        return audio_property

    def get_sample_rate(self, audio):
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
        :param audio_name: 音频名称，如 TRAIN/DR1/FCJF0/SA1_n.wav
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
        :param audio_name: 音频名称，如 TRAIN/DR1/FCJF0/SA1_n.wav
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
        if not os.path.exists(savingPath[0:savingPath.rfind("/")]):
            os.makedirs(savingPath[0:savingPath.rfind("/")])
        plt.savefig(savingPath)
        return savingPath

    def get_noise_audio_clips_list(self):
        """
        获取扰动音频列表
        :return: [TRAIN/DR1/FCJF0/SA1_n_gaussian_white_noise.wav]
        """
        noise_clips = glob.glob(self.noise_clips_path + "*/*/*/*.wav")
        for index in range(0, len(noise_clips)):
            noise_clips[index] = noise_clips[index].replace("\\", "/").replace(self.noise_clips_path, "")
        return noise_clips

    def get_pattern_summary(self):
        """
        获取扰动大类的详情
        :return:
        """
        pattern_summary = {}
        noise_clips = self.get_noise_audio_clips_list()
        for clip in noise_clips:
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
        :param pattern: 扰动类型
        :return:
        """
        pattern_type_summary = {}
        name = pattern_to_name[pattern]
        noise_clips = self.get_noise_audio_clips_list()
        for clip in noise_clips:
            if name in clip:
                if name == "gaussian_white_noise":
                    pattern_type = name
                else:
                    beg = clip.index(name) + len(name) + 1
                    end = clip.index(".")
                    pattern_type = clip[beg:end]
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
        noise_clips = self.get_noise_audio_clips_list()
        for clip in noise_clips:
            pattern_info = {"key": key}
            key += 1
            pattern_info["name"], pattern_tag = self.get_name_and_pattern_tag(clip)
            pattern_info["pattern"], pattern_info["patternType"] = get_pattern_info_from_pattern_tag(pattern_tag)
            audio_set_pattern.append(pattern_info)
        return audio_set_pattern

    def remove_current_noise_audio_clip(self, audio_name, pattern, pattern_type=None):
        """
        删除现有的扰动音频
        :param audio_name: 音频名称，如 TRAIN/DR1/FCJF0/SA1_n.wav
        :param pattern: 扰动类型
        :param pattern_type: 具体扰动
        :return:
        """
        audio_name = add_tag(audio_name, pattern_to_name[pattern])
        if pattern_type is not None:
            audio_name = add_tag(audio_name, pattern_type_to_suffix(pattern_type))
        os.remove(self.noise_clips_path + audio_name)

    def get_name_and_pattern_tag(self, name):
        """
        从扰动名字中获取原本的名字和扰动标签
        :param name: 扰动音频名称，TEST/DR1/FAKS0/SA2_n_human_sounds_respiratory_sounds.wav
        :return: TEST/DR1/FAKS0/SA2_n.wav,human_sounds_respiratory_sounds
        """
        return name[0:name.find("_n") + 2] + ".wav", name[name.find("_n") + 3:name.find(".")]

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
        audio_list = glob.glob(self.clips_path + "TEST/*/*/*.wav")
        audios = []
        for audio in audio_list:
            if get_audio_form(audio) == "wav":
                audios.append(audio.replace("\\", "/").replace(self.clips_path, ""))
        return audios

    def get_noise_testset_audio_clips_list(self):
        """
        获取测试集
        :return:
        """
        audio_list = glob.glob(self.noise_clips_path + "TEST/*/*/*.wav")
        audios = []
        for audio in audio_list:
            if get_audio_form(audio) == "wav":
                audios.append(audio.replace("\\", "/").replace(self.noise_clips_path, ""))
        return audios

    def get_trainset_audio_clips_list(self):
        """
        获取训练集
        :return:
        """
        audio_list = glob.glob(self.clips_path + "TRAIN/*/*/*.wav")
        audios = []
        for audio in audio_list:
            if get_audio_form(audio) == "wav":
                audios.append(audio.replace("\\", "/").replace(self.clips_path, ""))
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
        # pre_overall_wer, post_overall_wer = self.get_dataset_er()
        pre_overall_wer, post_overall_wer = round(self.wer_dict.get(model)[0], 3), round(
            self.wer_dict.get(model)[1], 3)
        validation_results.append({"preOverallER": pre_overall_wer})
        validation_results.append({"postOverallER": post_overall_wer})
        for index in range((int(page) - 1) * int(page_size), min(int(page) * int(page_size), len(audio_list))):
            audio_result = self.get_validation_result(audio_list[index], model)
            audio_result['key'] = index + 1
            validation_results.append(audio_result)
        return validation_results

    def get_validation_result(self, audio_name, model_name):
        """
        计算某一音频的所有验证内容
        :param audio_name: 音频名称，如 TRAIN/DR1/FCJF0/SA1_n.wav
        :param model_name: 模型名
        :return:
        """
        validation_result = {}
        validation_result['name'] = audio_name
        validation_result['realText'] = self.formalize(self.get_audio_clip_content(audio_name))
        validation_result['previousText'] = self.get_audio_clip_transcription(audio_name, model_name)
        validation_result['preER'] = round(wer(validation_result['realText'], validation_result['previousText']), 2)
        noise_audio_name = self.get_noise_clip_name(audio_name)
        validation_result['noise_audio_name'] = noise_audio_name
        validation_result['posteriorText'] = self.get_noise_audio_clip_transcription(noise_audio_name, model_name)
        validation_result['postER'] = round(wer(validation_result['realText'], validation_result['posteriorText']), 2)
        return validation_result

    def get_audio_clip_transcription(self, audio_name, model_name):
        """
        获取原音频识别出的内容
        :param audio_name: 音频名称，如 TRAIN/DR1/FCJF0/SA1_n.wav
        :param model_name: 模型名
        :return:
        """
        audio, rate = librosa.load(self.clips_path + audio_name, sr=16000)
        return self.get_transcription_by_models(model_name, audio, rate)

    def get_noise_audio_clip_transcription(self, audio_name, model_name):
        """
        获取扰动音频识别出的内容
        :param audio_name: 扰动音频名称，TEST/DR1/FAKS0/SA1_n_natural_sounds_wind.wav
        :param model_name:模型名
        :return:
        """
        audio, rate = librosa.load(self.noise_clips_path + audio_name, sr=16000)
        return self.get_transcription_by_models(model_name, audio, rate)

    def get_transcription_by_models(self, model_name, audio, sampling_rate):
        """
        由不同模型得出音频识别结果
        :param audio:
        :param sampling_rate:
        :param model_name:
        :return:
        """
        if model_name in self.model_dict.get("wav2vec2.0 Model"):
            input_values = self.processor(audio, sampling_rate=sampling_rate, return_tensors="pt").input_values
            logits = self.model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)
            return self.formalize(transcription[0])
        elif model_name in self.model_dict.get("S2T Model"):
            input_features = self.processor(audio, sampling_rate=sampling_rate, return_tensors="pt").input_features
            generated_ids = self.model.generate(input_features=input_features)
            transcription = self.processor.batch_decode(generated_ids)
            return self.formalize(transcription[0])
        elif model_name in self.model_dict.get("HuBert Model"):
            input_values = self.processor(audio, sampling_rate=sampling_rate, return_tensors="pt").input_values
            logits = self.model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.decode(predicted_ids[0])
            return self.formalize(transcription)
        elif model_name in self.model_dict.get("Data2Vec Model"):
            input_values = self.processor(audio, sampling_rate=sampling_rate, return_tensors="pt",
                                          padding="longest").input_values
            logits = self.model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)
            return self.formalize(transcription[0])
        elif model_name in self.model_dict.get("UniSpeech Model"):
            input_values = self.processor(audio, sampling_rate=sampling_rate, return_tensors="pt").input_values
            logits = self.model(input_values).logits
            prediction_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(prediction_ids)
            return transcription[0]

    def get_dataset_er(self, model_name):
        """
        获取数据集总体上的 WER/CER
        :param model_name: 模型名
        :return:
        """
        if len(self.real_text_list) == 0 or len(self.previous_text_list) == 0 or len(self.post_text_list) == 0:
            self.get_dataset_texts(model_name)
        return wer_overall(self.real_text_list, self.previous_text_list), wer_overall(self.real_text_list,
                                                                                      self.post_text_list)

    def get_dataset_texts(self, model_name):
        """
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
        if self.processor is None and self.model is None:
            if model_name in self.model_dict.get("wav2vec2.0 Model"):
                self.processor = AutoProcessor.from_pretrained(self.model_path + model_name)
                self.model = AutoModelForCTC.from_pretrained(self.model_path + model_name)
            elif model_name in self.model_dict.get("S2T Model"):
                self.processor = AutoProcessor.from_pretrained(self.model_path + model_name)
                self.model = AutoModelForSpeechSeq2Seq.from_pretrained(self.model_path + model_name)
            elif model_name in self.model_dict.get("HuBert Model"):
                self.processor = Wav2Vec2Processor.from_pretrained(self.model_path + model_name)
                self.model = HubertForCTC.from_pretrained(self.model_path + model_name)
            elif model_name in self.model_dict.get("Data2Vec Model"):
                self.processor = Wav2Vec2Processor.from_pretrained(self.model_path + model_name)
                self.model = Data2VecAudioForCTC.from_pretrained(self.model_path + model_name)
            elif model_name in self.model_dict.get("UniSpeech Model"):
                self.processor = AutoProcessor.from_pretrained(self.model_path + model_name)
                self.model = AutoModelForCTC.from_pretrained(self.model_path + model_name)
        return True

    def get_noise_clip_name(self, audio_name):
        """
        获取原音频对应的扰动音频名称
        :param audio_name: 音频名称，如 TRAIN/DR1/FCJF0/SA1_n.wav
        :return:
        """
        path = self.noise_clips_path + audio_name[0:audio_name.rfind("/") + 1]
        prefix = audio_name[audio_name.rfind("/") + 1:audio_name.find(".")]
        for file in os.listdir(path):
            if file.startswith(prefix):
                return audio_name[0:audio_name.rfind("/") + 1] + file

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
        规范化句子
        :param sentence: 识别出的内容
        :return:
        """
        sentence = sentence.lower().capitalize()
        CHARS_TO_IGNORE = [",", "-", "--", "?", "."]
        chars_to_ignore_regex = f"[{re.escape(''.join(CHARS_TO_IGNORE))}]"
        return re.sub(chars_to_ignore_regex, "", sentence)
