import glob

import librosa
import soundfile

from Dataset.AiShell.AiShellUtil import make_dirs
from Dataset.Dataset import Dataset
from Perturbation.AudioProcess import add_noise, quieter, change_pitch, louder, gaussian_white_noise
from Util.AudioUtil import AUDIO_SETS_PATH, NOISE_AUDIO_SETS_PATH, add_tag, get_source_noises_path, pattern_types_dict, \
    pattern_type_to_suffix, get_audio_form


class Thchs30(Dataset):
    def __init__(self, dataset):
        Dataset.__init__(self, dataset)
        self.dataset_path = AUDIO_SETS_PATH + dataset + "/"
        self.clips_path = AUDIO_SETS_PATH + dataset + "/"
        self.noise_clips_path = NOISE_AUDIO_SETS_PATH + dataset + "/"

    def add_gaussian_noise(self, audio_name):
        """
        添加高斯白噪声
        :param audio_name: test/S0764/BAC009S0764W0121.wav
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        noise_audio = sig + gaussian_white_noise(sig, snr=5)
        noise_audio_name = add_tag(audio_name, "gaussian_white_noise")
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)

    def add_sound_level(self, audio_name, pattern_type):
        """
        添加 sound level 扰动
        :param audio_name: test/S0764/BAC009S0764W0121.wav
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
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_natural_sounds(self, audio_name, pattern_type):
        """
        添加 natural sound 扰动
        :param audio_name: test/S0764/BAC009S0764W0121.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Natural sounds"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Natural Sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "natural_sounds"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_animal(self, audio_name, pattern_type):
        """
        添加 animal 扰动
        :param audio_name: test/S0764/BAC009S0764W0121.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Animal"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Animal", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "animal"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_sound_of_things(self, audio_name, pattern_type):
        """
        添加 sound of things 扰动
        :param audio_name: test/S0764/BAC009S0764W0121.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Sound of things"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Sound of things", pattern_type), sr=sr,
                                               mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "sound_of_things"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_human_sounds(self, audio_name, pattern_type):
        """
        添加 human sounds 扰动
        :param audio_name: 形如 test/S0764/BAC009S0764W0121.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Human sounds"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Human sounds", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "human_sounds"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_music(self, audio_name, pattern_type):
        """
        添加 music 扰动
        :param audio_name: 形如 test/S0764/BAC009S0764W0121.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Music"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Music", pattern_type), sr=sr, mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "music"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def add_source_ambiguous_sounds(self, audio_name, pattern_type):
        """
        添加 source_ambiguous_sounds 扰动
        :param audio_name: test/S0764/BAC009S0764W0121.wav
        :param pattern_type:
        :return:
        """
        sig, sr = librosa.load(self.clips_path + audio_name, sr=None)
        if pattern_type in pattern_types_dict.get("Source-ambiguous sounds"):
            noise_sig, noise_sr = librosa.load(get_source_noises_path("Source-ambiguous sounds", pattern_type), sr=sr,
                                               mono=True)
            noise_audio = add_noise(sig, noise_sig)
        else:
            return "patternType error"
        noise_audio_name = add_tag(add_tag(audio_name, "source_ambiguous_sounds"), pattern_type_to_suffix(pattern_type))
        noise_audio_path = self.noise_clips_path + noise_audio_name
        make_dirs(noise_audio_path)
        soundfile.write(noise_audio_path, noise_audio, sr)
        return ""

    def get_testset_audio_clips_list(self):
        testset_path = self.clips_path + "test/"
        audio_list = glob.glob(testset_path + "*.wav")
        audios = []
        for audio in audio_list:
            if get_audio_form(audio) == "wav":
                audios.append(audio.replace("\\", "/").replace(self.clips_path, ""))
        return audios
