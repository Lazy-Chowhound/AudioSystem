import glob

from Dataset.Dataset import Dataset
from Util.AudioUtil import AUDIO_SETS_PATH, NOISE_AUDIO_SETS_PATH, get_audio_form


class LibriSpeech(Dataset):
    def __init__(self, dataset):
        Dataset.__init__(self, dataset)
        self.dataset_path = AUDIO_SETS_PATH + dataset + "/"
        self.clips_path = AUDIO_SETS_PATH + dataset + "/"
        self.noise_clips_path = NOISE_AUDIO_SETS_PATH + dataset + "/"

    def get_testset_audio_clips_list(self):
        testset_path = self.clips_path + "test-clean/"
        audio_list = glob.glob(testset_path + "*/*/*.flac")
        audios = []
        for audio in audio_list:
            if get_audio_form(audio) == "flac":
                audios.append(audio.replace("\\", "/").replace(self.clips_path, ""))
        return audios
