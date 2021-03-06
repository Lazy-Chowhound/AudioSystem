import glob
import os

import librosa.display
import torch
from pydub import AudioSegment
from transformers import AutoProcessor, AutoModelForCTC, AutoModelForSpeechSeq2Seq, Wav2Vec2Processor, HubertForCTC, \
    Data2VecAudioForCTC

from Dataset.Dataset import Dataset
from Perturbation.AudioProcess import calculate_SNR
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
            "UniSpeech Model": ["unispeech-large-1500h-cv-timit"]}
        self.wer_dict = {"wav2vec2-large-960h": [0.09985528219971057, 0.23664806009234374],
                         "wav2vec2-large-lv60-timit-asr": [0.1386534353249259, 0],
                         "wav2vec2-base-timit-asr": [0.2555992006064365, 0],
                         "s2t-small-librispeech-asr": [0.10778030459651299, 0],
                         "s2t-medium-librispeech-asr": [0.11412032251395493, 0],
                         "s2t-large-librispeech-asr": [0.10281855144373234, 0.2819929708497002],
                         "hubert-large-ls960-ft": [0.06594996898904279, 0.15174695058920817],
                         "data2vec-audio-base-960h": [0.08765763903245813, 0.26951967472951555],
                         "unispeech-large-1500h-cv-timit": [0.23816415133347116, 0.4294673006684584]}
        self.wer_type = {
            "wav2vec2-large-960h": {"Animal": [0.08252818035426732, 0.27334943639291465],
                                    "Natural sounds": [0.0948782535684299, 0.22628043660789252],
                                    "Sound of things": [0.11092851273623665, 0.27074774034511095],
                                    "Human sounds": [0.10191347753743761, 0.2579034941763727],
                                    "Music": [0.10653222270933801, 0.1863217886891714],
                                    "Source-ambiguous sounds": [0.1025844930417495, 0.20318091451292247]}
        }

    def get_audio_clips_properties_by_page(self, page, page_size):
        """
        ??????????????????????????????
        :param page: ??????
        :param page_size: ????????????
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
        ????????????????????????????????????
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
        ????????????????????????????????????
        :param audio_name: ?????????????????? TRAIN/DR1/FCJF0/SA1_n.wav
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
        ??????????????????????????????
        :param audio_name: ?????????????????? TRAIN/DR1/FCJF0/SA1_n.wav
        :return:
        """
        audio = self.clips_path + audio_name
        audio_property = {}
        audio_property['name'] = audio_name
        audio_property['size'] = str(self.get_duration(audio)) + "???"
        audio_property['channel'] = "???" if self.get_channels(audio) == 1 else "???"
        audio_property['sampleRate'] = str(self.get_sample_rate(audio)) + "Hz"
        audio_property['bitDepth'] = str(self.get_bit_depth(audio)) + "bit"
        audio_property['content'] = self.get_audio_clip_content(audio_name)
        return audio_property

    def get_sample_rate(self, audio):
        """
        ????????????????????????
        :param audio: ??????????????????
        :return:
        """
        samplingRate = librosa.get_samplerate(audio)
        return samplingRate

    def get_duration(self, audio):
        """
        ??????????????????
        :param audio: ??????????????????
        :return:
        """
        sig, sr = librosa.load(audio, sr=None)
        return round(librosa.get_duration(sig, sr), 2)

    def get_channels(self, audio):
        """
        ????????????
        :param audio: ??????????????????
        :return:
        """
        song = AudioSegment.from_wav(audio)
        return song.channels

    def get_bit_depth(self, audio):
        """
        ????????????
        :param audio: ??????????????????
        :return:
        """
        song = AudioSegment.from_wav(audio)
        return song.sample_width * 8

    def get_noise_audio_clips_list(self):
        """
        ????????????????????????
        :return: [TRAIN/DR1/FCJF0/SA1_n_gaussian_white_noise.wav]
        """
        noise_clips = glob.glob(self.noise_clips_path + "*/*/*/*.wav")
        for index in range(0, len(noise_clips)):
            noise_clips[index] = noise_clips[index].replace("\\", "/").replace(self.noise_clips_path, "")
        return noise_clips

    def get_pattern_summary(self):
        """
        ???????????????????????????
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
        ??????????????????????????????????????????????????????????????????
        :param pattern: ????????????
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
        ?????????????????????????????????????????????????????????
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
            if pattern_info["pattern"] != "Sound level":
                pattern_info["snr"] = round(
                    calculate_SNR(self.clips_path + pattern_info["name"], self.noise_clips_path + clip), 2)
            else:
                pattern_info["snr"] = "???"
            audio_set_pattern.append(pattern_info)
        return audio_set_pattern

    def remove_current_noise_audio_clip(self, audio_name, pattern, pattern_type=None):
        """
        ???????????????????????????
        :param audio_name: ?????????????????? TRAIN/DR1/FCJF0/SA1_n.wav
        :param pattern: ????????????
        :param pattern_type: ????????????
        :return:
        """
        audio_name = add_tag(audio_name, pattern_to_name[pattern])
        if pattern_type is not None:
            audio_name = add_tag(audio_name, pattern_type_to_suffix(pattern_type))
        os.remove(self.noise_clips_path + audio_name)

    def get_name_and_pattern_tag(self, name):
        """
        ??????????????????????????????????????????????????????
        :param name: ?????????????????????TEST/DR1/FAKS0/SA2_n_human_sounds_respiratory_sounds.wav
        :return: TEST/DR1/FAKS0/SA2_n.wav,human_sounds_respiratory_sounds
        """
        return name[0:name.find("_n") + 2] + ".wav", name[name.find("_n") + 3:name.find(".")]

    def get_num_of_clips_and_noise_clips(self):
        """
        ??????????????????????????????????????????
        :return:
        """
        num_list = [len(self.get_audio_clips_list()), len(self.get_noise_audio_clips_list())]
        return num_list

    def get_testset_audio_clips_list(self):
        """
        ???????????????
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
        ???????????????
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
        ???????????????
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
        ????????????????????????
        :param model: ?????????
        :param page: ??????
        :param page_size: ????????????
        :return:
        """
        validation_results = []
        audio_list = self.get_testset_audio_clips_list()
        validation_results.append({"total": len(audio_list)})
        # ???????????? ???????????????????????????????????????
        # pre_overall_wer, post_overall_wer = self.get_dataset_er(model)
        pre_overall_wer, post_overall_wer = round(self.wer_dict.get(model)[0], 3), round(
            self.wer_dict.get(model)[1], 3)
        validation_results.append({"preOverallER": pre_overall_wer})
        validation_results.append({"postOverallER": post_overall_wer})
        for index in range((int(page) - 1) * int(page_size), min(int(page) * int(page_size), len(audio_list))):
            audio_result = self.get_validation_result(audio_list[index], model)
            audio_result['key'] = index + 1
            validation_results.append(audio_result)
        return validation_results

    def get_validation_results_by_pattern(self, pattern, model, page, page_size):
        """
        ?????????????????????????????????
        :param pattern: ????????????
        :param model: ?????????
        :param page: ??????
        :param page_size: ??????
        :return:
        """
        validation_results = []
        certain_pattern_audios = []
        audio_list = self.get_testset_audio_clips_list()
        pattern_name = pattern_to_name.get(pattern)
        for audio in audio_list:
            noise_audio_name = self.get_noise_clip_name(audio)
            if pattern_name in noise_audio_name:
                certain_pattern_audios.append(audio)

        validation_results.append({"total": len(certain_pattern_audios)})
        # ???????????? ???????????????????????????????????????
        # pre_overall_wer, post_overall_wer = self.get_certain_pattern_er(model,pattern)
        pre_overall_wer, post_overall_wer = round(self.wer_type.get(model).get(pattern)[0], 2), round(
            self.wer_type.get(model).get(pattern)[1], 2)
        validation_results.append({"preOverallER": pre_overall_wer})
        validation_results.append({"postOverallER": post_overall_wer})
        for index in range((int(page) - 1) * int(page_size),
                           min(int(page) * int(page_size), len(certain_pattern_audios))):
            audio_result = self.get_validation_result(certain_pattern_audios[index], model)
            audio_result['key'] = index + 1
            validation_results.append(audio_result)
        return validation_results

    def get_validation_result(self, audio_name, model_name):
        """
        ???????????????????????????????????????
        :param audio_name: ?????????????????? TRAIN/DR1/FCJF0/SA1_n.wav
        :param model_name: ?????????
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
        ?????????????????????????????????
        :param audio_name: ?????????????????? TRAIN/DR1/FCJF0/SA1_n.wav
        :param model_name: ?????????
        :return:
        """
        audio, rate = librosa.load(self.clips_path + audio_name, sr=16000)
        return self.get_transcription_by_models(model_name, audio, rate)

    def get_noise_audio_clip_transcription(self, audio_name, model_name):
        """
        ????????????????????????????????????
        :param audio_name: ?????????????????????TEST/DR1/FAKS0/SA1_n_natural_sounds_wind.wav
        :param model_name:?????????
        :return:
        """
        audio, rate = librosa.load(self.noise_clips_path + audio_name, sr=16000)
        return self.get_transcription_by_models(model_name, audio, rate)

    def get_transcription_by_models(self, model_name, audio, sampling_rate):
        """
        ???????????????????????????????????????
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
        ??????????????????????????? WER/CER
        :param model_name: ?????????
        :return:
        """
        real, previous, post = [], [], []
        audio_list = self.get_testset_audio_clips_list()
        for audio in audio_list:
            real.append(self.formalize(self.get_audio_clip_content(audio)))
            previous.append(self.get_audio_clip_transcription(audio, model_name))
            noise_audio = self.get_noise_clip_name(audio)
            post.append(self.get_noise_audio_clip_transcription(noise_audio, model_name))
        return wer_overall(real, previous), wer_overall(real, post)

    def get_certain_pattern_er(self, model_name, pattern):
        """
        ????????????????????????????????????
        :param model_name:
        :param pattern:
        :return:
        """
        real, previous, post = [], [], []
        certain_pattern_audios = []
        audio_list = self.get_testset_audio_clips_list()
        pattern_name = pattern_to_name.get(pattern)
        for audio in audio_list:
            noise_audio_name = self.get_noise_clip_name(audio)
            if pattern_name in noise_audio_name:
                certain_pattern_audios.append(audio)

        for audio in certain_pattern_audios:
            real.append(self.formalize(self.get_audio_clip_content(audio)))
            previous.append(self.get_audio_clip_transcription(audio, model_name))
            noise_audio = self.get_noise_clip_name(audio)
            post.append(self.get_noise_audio_clip_transcription(noise_audio, model_name))
            print(audio + "?????????")
        return wer_overall(real, previous), wer_overall(real, post)

    def load_model(self, model_name):
        """
        ????????????
        :param model_name: ?????????
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
        ??????????????????????????????????????????
        :param audio_name: ?????????????????? TRAIN/DR1/FCJF0/SA1_n.wav
        :return:
        """
        path = self.noise_clips_path + audio_name[0:audio_name.rfind("/") + 1]
        prefix = audio_name[audio_name.rfind("/") + 1:audio_name.find(".")]
        for file in os.listdir(path):
            if file.startswith(prefix):
                return audio_name[0:audio_name.rfind("/") + 1] + file

    def judge_model(self, model):
        """
        ???????????????????????????????????????
        :param model: ?????????
        :return:
        """
        for (key, value) in self.model_dict.items():
            if model in value:
                return True
        return False

    def formalize(self, sentence):
        """
        ???????????????
        :param sentence: ??????????????????
        :return:
        """
        sentence = sentence.lower().capitalize()
        CHARS_TO_IGNORE = [",", "-", "--", "?", "."]
        chars_to_ignore_regex = f"[{re.escape(''.join(CHARS_TO_IGNORE))}]"
        return re.sub(chars_to_ignore_regex, "", sentence)
