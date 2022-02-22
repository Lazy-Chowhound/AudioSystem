import os

import librosa.display
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pydub import AudioSegment

from Util.AudioUtil import AUDIO_SETS_PATH, WAVEFORM_GRAPH_PATH, MEL_SPECTRUM_PATH


class CommonVoiceDataset:
    def __init__(self, dataset):
        self.dataset = dataset
        self.clips_path = AUDIO_SETS_PATH + dataset + "/clips/"
        self.dataset_path = AUDIO_SETS_PATH + dataset + "/"

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
        :param audio: 音频路径
        :return:
        """
        samplingRate = librosa.get_samplerate(audio)
        return samplingRate

    def get_duration(self, audio):
        """
        获取音频时长
        :param audio: 音频路径
        :return:
        """
        sig, sr = librosa.load(audio, sr=None)
        return round(librosa.get_duration(sig, sr), 2)

    def get_channels(self, audio):
        """
        获取声道
        :param audio: 音频路径
        :return:
        """
        song = AudioSegment.from_mp3(audio)
        return song.channels

    def get_bit_depth(self, audio):
        """
        获取位深
        :param audio: 音频路径
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
