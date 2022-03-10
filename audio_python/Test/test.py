from Dataset.CommonVoiceDataset.CommonVoiceDataset import CommonVoiceDataset


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
    pass
