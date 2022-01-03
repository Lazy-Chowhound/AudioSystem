import os
import librosa.display
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pydub import AudioSegment


# 获取音频所有属性
# path形如D:/AudioSystem/Audio/cv-corpus-chinese/
def getAudioProperty(path, audioName):
    audio = path + "clips/" + audioName
    audioProperty = {}
    detail = getAudioDetail(path, audioName)
    audioProperty['name'] = audioName
    audioProperty['size'] = str(getDuration(audio)) + "秒"
    audioProperty['gender'] = detail['gender']
    audioProperty['age'] = detail['age']
    audioProperty['channel'] = "单" if getChannels(audio) == 1 else "双"
    audioProperty['sampleRate'] = str(getSamplingRate(audio)) + "Hz"
    audioProperty['bitDepth'] = str(getBitDepth(audio)) + "bit"
    audioProperty['content'] = detail['sentence']
    return audioProperty


# 获取目录下所有音频文件名
def getAudioList(path):
    audioList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp3':
                audioList.append(file)
    return audioList


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
# path形如D:/AudioSystem/Audio/cv-corpus-chinese/clips/
def getWaveForm(path, audioName):
    audio = path + audioName
    sig, sr = librosa.load(audio, sr=None)
    plt.figure(figsize=(8, 5))
    librosa.display.waveshow(sig, sr=sr)
    plt.ylabel('Amplitude')
    savingPath = "WaveImage/" + audioName + ".jpg"
    plt.savefig(savingPath)
    return os.getcwd() + "/" + savingPath


# Mel频谱图
# path形如D:/AudioSystem/Audio/cv-corpus-chinese/clips/
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
    savingPath = "SpectrumImage/" + audioName + ".jpg"
    plt.savefig(savingPath)
    return os.getcwd() + "/" + savingPath


# 音频的采样率
def getSamplingRate(audio):
    samplingRate = librosa.get_samplerate(audio)
    return samplingRate


# 音频时长
def getDuration(audio):
    sig, sr = librosa.load(audio, sr=None)
    return librosa.get_duration(sig, sr)


# 声道
def getChannels(audio):
    song = AudioSegment.from_mp3(audio)
    return song.channels


# 位深
def getBitDepth(audio):
    song = AudioSegment.from_mp3(audio)
    return song.sample_width * 8


# 删除图片
def removeImage(path):
    os.remove(path)


if __name__ == '__main__':
    path = getWaveForm("D:/AudioSystem/Audio/cv-corpus-chinese/clips/", "common_voice_zh-CN_18524189.mp3")
    print(path)
    removeImage(path)
