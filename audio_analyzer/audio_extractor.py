from __future__ import unicode_literals

from typing import Any, List, Dict

from pytube import YouTube
from manual_analysis import danceability_timestamps

import os

cwd = os.getcwd()


def extract_audio(ytpath: str) -> Dict[str, Any]:
    try:
        yt: YouTube = YouTube(ytpath)
        video = yt.streams.filter(only_audio=True).first()
        video.download(output_path='./', filename='tmp.mp4')

        d: List[Dict[str, Any]] = danceability_timestamps('./tmp.mp4')
        os.remove('./tmp.mp4')

        return {"data": d}
    except Exception as e:
        print(e)
        return {"data": []}
