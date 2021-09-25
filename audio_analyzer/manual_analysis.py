from typing import Any, Dict, List
import numpy as np

import essentia.standard as es

SAMPLE_RATE: int = 44100

FRAME_LENGTH_SECONDS: int = 30

FRAME_LENGTH: int = FRAME_LENGTH_SECONDS * SAMPLE_RATE

CHILL_DANCEABLE_LOW_THRESHOLD: float = 1.25


def danceability_timestamps(filepath: str) -> List[Dict[str, Any]]:
    """
    Returns a dict with start and end times of the fragment and whether the
    fragment is danceable
    :param filepath:
    :return:
    """

    danceability_measurement: es.Danceability = es.Danceability()
    dynamic_complexity_measurement: es.DynamicComplexity = es.DynamicComplexity(frameSize=FRAME_LENGTH_SECONDS)
    rhythm: es.RhythmExtractor = es.RhythmExtractor()
    flatness_measurement: es.Flatness = es.Flatness()

    audio = es.EasyLoader(filename=filepath)()
    elapsed: int = 0
    timestamps: List[Dict[str, Any]] = []

    for frame in es.FrameGenerator(audio, FRAME_LENGTH, hopSize=FRAME_LENGTH):
        try:
            danceability, _ = danceability_measurement(frame)
            bpm, _, _, _ = rhythm(frame)
            _, avg_db_deviation = dynamic_complexity_measurement(frame)
            flatness = flatness_measurement(frame)

            elapsed += FRAME_LENGTH_SECONDS
            print(f'{elapsed} seconds')
            timestamps.append(
                {"start": elapsed - FRAME_LENGTH_SECONDS,
                 "end": elapsed,
                 "danceability": np.round(danceability, 2),
                 "avg_db_deviation": np.round(avg_db_deviation, 2),
                 "bpm": np.round(bpm, 2),
                 "flatness": flatness
                 }
            )
        except Exception as e:
            print(f'Exception while analyzing frames: {e}')
            break

    del danceability_measurement
    del dynamic_complexity_measurement
    del rhythm
    del audio

    return timestamps
