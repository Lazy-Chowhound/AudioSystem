import glob
import os
import random

from Dataset.CommonVoiceDataset.CommonVoiceDataset import CommonVoiceDataset
from Perturbation.AddNoisePattern import add_music


def get_text(order, model, start, end):
    cvd = CommonVoiceDataset("cv-corpus-chinese")
    test_list = cvd.get_testset_audio_clips_list()
    cvd.load_model(model)
    error_list = []
    for audio in test_list[start:end]:
        try:
            with open("../Dataset/CommonVoiceDataset/previousText" + str(order) + ".txt", "a", encoding="utf-8") as f:
                txt = cvd.get_audio_clip_transcription(audio)
                f.writelines(audio + " " + txt + "\n")
        except Exception:
            error_list.append(audio)
    print(error_list)


def get_noise_text(order, model, start, end):
    cvd = CommonVoiceDataset("cv-corpus-chinese")
    test_list = cvd.get_testset_audio_clips_list()
    cvd.load_model(model)
    error_list = []
    for audio in test_list[start:end]:
        noise_audio = cvd.get_noise_clip_name(audio)
        try:
            with open("../Dataset/CommonVoiceDataset/postText" + str(order) + ".txt", "a", encoding="utf-8") as f:
                txt = cvd.get_noise_audio_clip_transcription(noise_audio)
                f.writelines(noise_audio + " " + txt + "\n")
        except Exception:
            error_list.append(noise_audio)
    print(error_list)


if __name__ == '__main__':
    music_pattern_types = ["Musical instrument", "Music genre", "Musical concepts", "Music role", "Music mood"]
    audio_list = glob.glob(r"D:/AudioSystem/NoiseAudio/timit/lisa/data/timit/raw/TIMIT/*/*/*/*.wav")
    wanted_list = []
    for audio in audio_list:
        if "level" in audio:
            wanted_list.append(audio)
    change_list = random.choices(wanted_list, k=50)
    for audio in change_list[0:50]:
        try:
            audio = audio.replace("\\", "/")
            beg = audio.find("TEST")
            if beg == -1:
                beg = audio.find("TRAIN")
            source_audio = audio[beg:audio.find("_n") + 2] + ".wav"
            os.remove(audio)
            add_music("timit", source_audio, music_pattern_types[random.randint(0, len(music_pattern_types) - 1)])
        except Exception as e:
            print(audio)
