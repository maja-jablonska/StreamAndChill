from __future__ import unicode_literals
from re import sub

from typing import Any, List, Dict

from pytube import YouTube
from manual_analysis import danceability_timestamps
from musiccnn import load_ckpt_model, check_if_aggressive

import os
import subprocess


cwd = os.getcwd()
_MODEL_PATH = './hackzurich.savedmodel'
_model = load_ckpt_model(_MODEL_PATH)


def convert_to_mp3(src_file, target_file) -> None:
    assert(subprocess.run([
        'ffmpeg', '-i', src_file, '-vn', '-acodec', 'libmp3lame', '-ac',
         '2', '-ab', '160k', '-ar', '48000', target_file
    ]).returncode == 0)


def extract_audio(ytpath: str) -> Dict[str, Any]:

    target_mp4 = 'tmp.mp4'
    target_mp3 = 'tmp.mp3'

    try:
        yt: YouTube = YouTube(ytpath)
        video = yt.streams.filter(only_audio=True).first()
        video.download(output_path='./', filename='tmp.mp4')

        video.download(output_path='./', filename=target_mp4)
        convert_to_mp3(target_mp4, target_mp3)

        print("Converted")

        is_aggresive: bool = check_if_aggressive(_model, target_mp3)

        d: List[Dict[str, Any]] = danceability_timestamps('./tmp.mp4')
        os.remove('./tmp.mp4')
        os.remove('./tmp.mp3')

        return {"timestamps": d, "aggresive": bool(is_aggresive.numpy())}
    except Exception as e:
        print(f'Exception! {e}')
        return {"timestamps": [], "aggresive": True}
