from functools import lru_cache
from os import environ

from flask import Flask
from audio_extractor import extract_audio

app = Flask(__name__)


@app.route("/<video_id>")
def hello_world(video_id: str):
    return request_audio_extractor(video_id)


@lru_cache(maxsize=32)
def request_audio_extractor(video_id: str):
    return extract_audio(f'https://www.youtube.com/watch?v={video_id}')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=environ.get("PORT", 5000))
