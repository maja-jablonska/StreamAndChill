from __future__ import unicode_literals

from typing import List, Tuple, Dict

from pytube import YouTube
from manual_analysis import danceability_timestamps

import os
cwd = os.getcwd()


def extract_audio(ytpath: str) -> str:

    yt: YouTube = YouTube(ytpath)
    video = yt.streams.filter(only_audio=True).first()
    video.download(output_path='./', filename='tmp.mp4')

    d: List[Tuple[Tuple[int, int], Dict[str, float]]] = danceability_timestamps('./tmp.mp4')
    os.remove('./tmp.mp4')

    return str(d)
