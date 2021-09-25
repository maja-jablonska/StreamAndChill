from flask import Flask
from audio_extractor import extract_audio


app = Flask(__name__)


@app.route("/<video_id>")
def hello_world(video_id: str):
    return extract_audio(f'https://www.youtube.com/watch?v={video_id}')


if __name__ == "__main__":
    app.run()
