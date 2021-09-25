from __future__ import unicode_literals

from pytube import YouTube
from manual_analysis import danceable

import os
cwd = os.getcwd()


def extract_audio(ytpath: str) -> str:

    yt: YouTube = YouTube(ytpath)
    video = yt.streams.filter(only_audio=True).first()
    video.download(output_path='./', filename='tmp.mp4')

    d: bool = danceable('./tmp.mp4')
    os.remove('./tmp.mp4')

    return str(d)
