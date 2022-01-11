import json
import os

patterns = {"Gaussian noise": "gaussian_white_noise", "Sound level": "sound_level",
            "animal": "animal", "Source-ambiguous\nsounds": "source_ambiguous_sounds",
            "Natural Sounds": "natural_sounds", "Sound of things": "sound_of_things",
            "Human Sounds": "human_sounds", "Music": "music"}


def getNoisePatternSummary(dataset):
    path = "D:/AudioSystem/NoiseAudio/" + dataset + "/clips"
    summary = {}
    for file in os.listdir(path):
        for key, value in patterns.items():
            if value in file:
                if key in summary.keys():
                    summary[key] = summary[key] + 1
                else:
                    summary[key] = 1
                break
    return json.dumps(summary, ensure_ascii=False)


def getNoisePatternDetail(dataset, patternType):
    path = "D:/AudioSystem/NoiseAudio/" + dataset + "/clips"
    summaryDetail = {}
    name = patterns[patternType]
    for file in os.listdir(path):
        if name in file:
            if name == "gaussian_white_noise":
                pattern = name
            else:
                beg = file.index(name) + len(name) + 1
                end = file.index(".")
                pattern = file[beg:end]
            if pattern in summaryDetail.keys():
                summaryDetail[pattern] = summaryDetail[pattern] + 1
            else:
                summaryDetail[pattern] = 1
    return json.dumps(summaryDetail, ensure_ascii=False)


if __name__ == "__main__":
    print(getNoisePatternDetail("cv-corpus-chinese", "Sound level"))
