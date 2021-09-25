from __future__ import unicode_literals
from re import sub

from typing import List, Tuple, Dict

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

def extract_audio(ytpath: str) -> str:
    yt: YouTube = YouTube(ytpath)
    video = yt.streams.filter(only_audio=True).first()

    target_mp4 = 'tmp.mp4'
    target_mp3 = 'tmp.mp3'

    video.download(output_path='./', filename=target_mp4)
    convert_to_mp3(target_mp4, target_mp3)
    is_aggresive = check_if_aggressive(_model, target_mp3)
    if is_aggresive:
        return str(False)

    d: List[Tuple[Tuple[int, int], Dict[str, float]]] = danceability_timestamps(target_mp4)
    os.remove(target_mp4)

    return str(d)
