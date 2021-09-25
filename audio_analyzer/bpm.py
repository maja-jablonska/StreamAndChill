import essentia.standard as es
from typing import Dict


def detect_bpm(filepath: str) -> Dict[str, float]:
    print("Detecting bpm...")
    features, features_frames = es.MusicExtractor(rhythmStats=['mean', 'stdev'])(filepath)
    return {"bpm": float(features["rhythm.bpm"]),
            "beats_count_per_length": float(features["rhythm.beats_count"]) / float(
                features["metadata.audio_properties.analysis.length"]),
            "danceability": float(features["rhythm.danceability"])}
