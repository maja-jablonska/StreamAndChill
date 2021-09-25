from __future__ import unicode_literals
import youtube_dl

import os
cwd = os.getcwd()


def remove_temp_files():
    for item in os.listdir(os.curdir):
        if item.endswith(".mp3"):
            os.remove(item)


def extract_audio(ytpath: str) -> str:
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([ytpath])
        print(ydl)

    remove_temp_files()
    return "Done downloading"
