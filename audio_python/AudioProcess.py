import json
import librosa.display
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pydub import AudioSegment


# 获取指定音频的详情
# path形如D:/AudioSystem/Audio/cv-corpus-chinese/
def getAudioDetail(path, audioName):
    files = ['validated.tsv', 'invalidated.tsv', 'other.tsv']
    detail = {}
    for file in files:
        train = pd.read_csv(path + file, sep='\t', header=0)
        for index, row in train.iterrows():
            if audioName in row['path']:
                detail['id'] = index
                for item in row.items():
                    detail[item[0]] = item[1]
                break
    return detail


# 波形图、振幅
def getWaveForm(path, audioName):
    audio = path + audioName
    sig, sr = librosa.load(audio, sr=None)
    plt.figure(figsize=(8, 5))
    librosa.display.waveshow(sig, sr=sr)
    plt.ylabel('Amplitude')
    plt.savefig("WaveImage/" + audioName + ".jpg")
    plt.show()


# Mel频谱图
def getSpectrum(path, audioName):
    audio = path + audioName
    sig, sr = librosa.load(audio, sr=None)
    S = librosa.feature.melspectrogram(y=sig, sr=sr)
    plt.figure(figsize=(8, 5))
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
                             y_axis='mel', fmax=8000, x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    plt.savefig("SpectrumImage/" + audioName + ".jpg")
    plt.show()


# 音频的采样率
def getSamplingRate(path, audioName):
    audio = path + audioName
    samplingRate = librosa.get_samplerate(audio)
    return samplingRate


# 音频时长
def getDuration(path, audioName):
    audio = path + audioName
    sig, sr = librosa.load(audio, sr=None)
    return librosa.get_duration(sig, sr)


# 声道
def getChannels(path, audioName):
    audio = path + audioName
    song = AudioSegment.from_mp3(audio)
    return song.channels


# 位深
def getBitDepth(path, audioName):
    audio = path + audioName
    song = AudioSegment.from_mp3(audio)
    return song.sample_width * 8
