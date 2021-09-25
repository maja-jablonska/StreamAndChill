from typing import Dict, Tuple

import essentia.standard as es

SAMPLE_RATE: int = 44100

FRAME_LENGTH_SECONDS: int = 30

FRAME_LENGTH: int = FRAME_LENGTH_SECONDS*SAMPLE_RATE

CHILL_DANCEABLE_LOW_THRESHOLD: float = 1.25


def danceability_timestamps(filepath: str) -> Dict[Tuple[int, int], float]:
    """
    Returns a dict with start and end times of the fragment and whether the
    fragment is danceable
    :param filepath:
    :return:
    """
    audio = es.MonoLoader(filename=filepath)()
    elapsed: int = 0
    timestamps: Dict[Tuple[int, int], bool] = {}

    for frame in es.FrameGenerator(audio, FRAME_LENGTH, hopSize=FRAME_LENGTH):
        danceability, _ = es.Danceability()(frame)

        elapsed += FRAME_LENGTH_SECONDS
        print(f'{elapsed} seconds')
        timestamps[(elapsed-FRAME_LENGTH_SECONDS, elapsed)] = danceability

    return timestamps
