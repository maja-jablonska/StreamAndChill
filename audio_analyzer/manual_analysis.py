from typing import Dict, Tuple, List

import essentia.standard as es

SAMPLE_RATE: int = 44100

FRAME_LENGTH_SECONDS: int = 30

FRAME_LENGTH: int = FRAME_LENGTH_SECONDS*SAMPLE_RATE

CHILL_DANCEABLE_LOW_THRESHOLD: float = 1.25


danceability: es.Danceability = es.Danceability()
beats_loudness: es.BeatsLoudness = es.BeatsLoudness()


def danceability_timestamps(filepath: str) -> List[Tuple[Tuple[int, int], float]]:
    """
    Returns a dict with start and end times of the fragment and whether the
    fragment is danceable
    :param filepath:
    :return:
    """
    audio = es.MonoLoader(filename=filepath)()
    elapsed: int = 0
    timestamps: List[Tuple[Tuple[int, int], float]] = []

    for frame in es.FrameGenerator(audio, FRAME_LENGTH, hopSize=FRAME_LENGTH):
        danceability, _ = danceability(frame)

        elapsed += FRAME_LENGTH_SECONDS
        print(f'{elapsed} seconds')
        timestamps.append(
            ((elapsed-FRAME_LENGTH_SECONDS, elapsed), danceability)
        )

    return timestamps
