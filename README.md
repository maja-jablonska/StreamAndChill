# HackZurich2021

## Inspiration

How much time do we spend in front of the computer? This is a question that has already been asked too many times, but we couldn't resist. Without a doubt, people spend a big part of their leisure time on YouTube and other streaming services, watching cute cats, listening to chillhop.
It's still difficult to let go of stress though - this is the reason why we decided to develop Stream & Chill, a solution that synchronizes with your habits and reminds you to take self-care to the next level.

## What it does

Stream & Chill is about reminding you about self-care at the moment you dedicate to yourself in form of a humble browser extension. Its task is to analyze the currently watched video and determine if it's one of the calmer kinds - so that it can boost your YOU time with some breathing exercises.

## How we built it

### Audio processing

#### Retrieving the audio of currently watched video

The easy part - we used [pytube](https://github.com/pytube/pytube) and worked with temporary mp3 files.

#### Signal analysis

We decided to use some traditional signal analysis techniques. Despite the vast variety of music genres a few technical features were extracted to support the machine learning process, e.g. by discarding songs that are definitely fast or have a large variance of loudness. This has been achieved using [essentia](https://essentia.upf.edu/).

The signal was analyzed in the form of 30 second long chunks - large fragments aren't very informative in terms of pace and beat since everything is averaged, including intro and outro which tend to be much quieter and slower.

Extracted features:
- **danceability** - was derived using the algorithm described in work [1].
- **bpm** - beats per second are an obvious measure, although it does depend on meter
- **average dB variance** - this can be interpreted as the average change in loudness. This is important in the case of songs that feature strong bass drops or heavy beats.

#### Machine learning - mood estimation

In order to determine if the song is _calm_ we trained a binary classifier.

Dataset was built using 30 second long chunks of various mixtapes we have subjectively labeled as calm (lo-fi, slow pop, chillhop, meditation music) or aggressive (metal, techno, fast hip-hop, club music). Due to time limits and the fact that we didn't use any pretrained checkpoint, we had to use small dataset (~1500 30s samples) targeting some boundary subsets for these genres.

The core of the model is a convolutional neural network, similar to the Pons, J. and Serra, X., 2019. musicnn: Pre-trained convolutional neural networks for music audio tagging which works on sound spectrograms.

The core of the model is a convolutional neural network, similar to [2].

#### Putting it all together: python webservice

We are serving the estimates using a webservice based on the framework [flask](https://flask.palletsprojects.com/en/2.0.x/).

There is just a single GET endpoint which accepts ```video_id```, processes the video's audio and returns the following JSON:

```
GET /<video_id>
```

Response:

```
{
  "timestamps": [
    {
      "start": beginning of the fragment in seconds,
      "end": end of the fragment in seconds,
      "avg_db_deviation": average dB deviation as float,
      "bpm": beats per minute as float,
      "danceability": danceability index as float,
    }, ...
  ],
  "aggresive": boolean
}
```

## Challenges we ran into

Determining the mood of the music is definitely a challenging task! Mood depends on so many features and is very difficult to quantify. Consider some particular examples, such as slow metal songs, which have low bpm and yet are heavy and powerful. On the other hand, some lo-fi tracks can have a fast beat underneath, yet they are relaxing and pleasant.

This is a great case for machine learning! After all, we are able to build a dataset and decide what do we consider as calm. To make the challenge more feasible we focused on rather concrete (one could even say, extreme) examples of the two types of music.

## Accomplishments that we're proud of

In our opinion training, a model overnight is a success - even despite the task being binary classification it was rather difficult to tackle.
Moreover, combining it with technical signal analysis results allowed us to estimate the mood with satisfactory confidence.

## What we learned

- Signal analysis proved to be a very interesting domain that's a bridge between music and maths - it was very enjoyable to build the feature extraction pipeline!

## What's next for Stream & Chill

There is so much more in the streaming world - Netflix, HBO GO, Amazon Prime - that's just to name a few! Our goal and dream is to connect Stream & Chill to as many as possible.

**References**
[1] Streich, S. and Herrera, P., Detrended Fluctuation Analysis of Music Signals: Danceability Estimation and further Semantic Characterization, Proceedings of the AES 118th Convention, Barcelona, Spain, 2005

[2] Pons, J. and Serra, X., 2019. musicnn: Pre-trained convolutional neural networks for music audio tagging which works on sound spectrograms

---

# Deployment

## Local build

### Flask server

Everything needed for the server is in the ```/audio analyzer``` directory.

1. Install Aptfile requirements with apt-get
2. Install pip requirements from requirements.txt
3. Start flask server with ```python server.py```

#### Deploying of Heroku

It is adjusted for Heroku deployment, you just need to remember about specific buildpacks:

```
heroku buildpacks:add --index 1 https://github.com/dwnld/heroku-buildpack-ffmpeg.git -a dreamteamzurich
heroku buildpacks:add --index 1 heroku/python -a dreamteamzurich
```

To push use command line from the root directory:

```
git subtree push --prefix audio_analyzer heroku main
```
