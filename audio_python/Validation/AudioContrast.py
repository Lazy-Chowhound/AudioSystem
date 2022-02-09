import json
import os

import pandas as pd

from Audio.AudioProperty import get_audio_clips_list
from Util.Annotation import rpcApi
from Util.AudioUtil import get_audio_set_path
from Util.RpcResult import RpcResult


@rpcApi
def get_audio_set_contrast_content_by_page(dataset, page, page_size):
    """
    分页获取对比内容
    :param dataset:
    :param page:
    :param page_size:
    :return:
    """
    contrast_content = []
    audio_clips_list = get_audio_clips_list(dataset)
    contrast_content.append({'total': len(audio_clips_list)})
    for i in range((int(page) - 1) * int(page_size), min(int(page) * int(page_size), len(audio_clips_list))):
        audio_name = audio_clips_list[i]
        audio_contrast_content = {'key': i + 1}
        audio_contrast_content.update(get_audio_clips_contrast_content(dataset, audio_name))
        contrast_content.append(audio_contrast_content)
    return RpcResult.ok(json.dumps(contrast_content, ensure_ascii=False))


def get_audio_clips_contrast_content(dataset, audio_name):
    """
    获取指定音频前后对比的详情
    :param dataset:
    :param audio_name:
    :return:
    """
    contrast_content = {'name': audio_name}
    pre_content = get_audio_clip_previous_content(dataset, audio_name)
    post_content = get_audio_clip_posterior_content(dataset, audio_name)
    contrast_content['preContent'] = pre_content
    contrast_content['postContent'] = post_content
    return contrast_content


def get_audio_clip_previous_content(dataset, audio_name):
    """
    获取指定音频先前的详情
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :return:
    """
    path = get_audio_set_path(dataset)
    files = ['validated.tsv', 'invalidated.tsv', 'other.tsv']
    for file in files:
        train = pd.read_csv(os.path.join(path, file), sep='\t', header=0)
        for index, row in train.iterrows():
            if audio_name in row['path']:
                props = dict(row.items())
                return props['sentence']


def get_audio_clip_posterior_content(dataset, audio_name):
    """
    获取指定音频扰动之后的详情
    :param dataset: cv-corpus-chinese
    :param audio_name: common_voice_zh-CN_18524189.mp3
    :return:
    """
    return "xxx"


if __name__ == '__main__':
    print(get_audio_set_contrast_content_by_page("cv-corpus-chinese", 1, 5).data)
