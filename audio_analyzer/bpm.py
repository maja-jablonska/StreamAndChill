import essentia.standard as es

SAMPLE_RATE: int = 44100

FRAME_LENGTH: int = 30

# If something is chill for 5 minutes, we decide it's chill.
MIN_CHILL_TIME: int = 10*FRAME_LENGTH
HOP_SIZE: int = int()

CHILL_DANCEABLE_LOW_THRESHOLD: float = 1.25


def danceable(filepath: str) -> bool:
    audio = es.MonoLoader(filename=filepath)()
    elapsed: int = 0

    for frame in es.FrameGenerator(audio, SAMPLE_RATE*FRAME_LENGTH):
        print("Detecting danceability...")
        danceability, _ = es.Danceability()(frame)
        if danceability > CHILL_DANCEABLE_LOW_THRESHOLD:
            print(f'Oh! {danceability}')
            return True

        elapsed += FRAME_LENGTH

        print(danceability)
        if elapsed > MIN_CHILL_TIME:
            return False

