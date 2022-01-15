import soundfile

from AudioProcess import *
from Util.util import *


def add_gaussian_noise(path, audioName):
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = gaussian_white_noise(sig, snr=5)
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    waveName = audioName.replace(".mp3", ".wav")
    noiseWaveName = addTag(waveName, "gaussian_white_noise")
    soundfile.write(wavePath + noiseWaveName, noiseAudio, sr)
    trans_wav_to_mp3(wavePath, noiseWaveName)
    removeAudio(wavePath, noiseWaveName)


def add_sound_level(path, audioName, specificPattern=None):
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = sig
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    if specificPattern == "louder":
        noiseAudio = louder(sig)
    elif specificPattern == "quieter":
        noiseAudio = quieter(sig)
    elif specificPattern == "pitch":
        noiseAudio = changePitch(sig, sr)
    elif specificPattern == "speed":
        sr = sr * 2
    noiseWaveName = addTag(addTag(audioName, "sound_level"), specificPattern).replace(".mp3", ".wav")
    soundfile.write(wavePath + noiseWaveName, noiseAudio, sr)
    trans_wav_to_mp3(wavePath, noiseWaveName)
    removeAudio(wavePath, noiseWaveName)


def add_natural_sounds(path, audioName, specificPattern=None):
    sig, sr = librosa.load(path + audioName, sr=None)
    noiseAudio = sig
    wavePath = path.replace("D:/AudioSystem/Audio/", "D:/AudioSystem/noiseAudio/")
    if specificPattern == "wind":
        noiseSig, noise_sr = librosa.load("D:/AudioSystem/Noise/mechanism.wav", sr=sr, mono=True)
        noiseAudio = louder(sig)
    elif specificPattern == "thunderstorm":
        noiseAudio = quieter(sig)
    elif specificPattern == "water":
        noiseAudio = changePitch(sig, sr)
    elif specificPattern == "fire":
        sr = sr * 2
    noiseWaveName = addTag(addTag(audioName, "natural_sounds"), specificPattern).replace(".mp3", ".wav")
    soundfile.write(wavePath + noiseWaveName, noiseAudio, sr)
    trans_wav_to_mp3(wavePath, noiseWaveName)
    removeAudio(wavePath, noiseWaveName)


if __name__ == '__main__':
    add_gaussian_noise1("D:/AudioSystem/Audio/cv-corpus-chinese/clips/", "common_voice_zh-CN_18524189.mp3")
