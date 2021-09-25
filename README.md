# HackZurich2021

## Deploying audio_analyzer to heroku

Remeber to add the Aptfile buildpack:

```
heroku buildpacks:add --index 1 https://github.com/dwnld/heroku-buildpack-ffmpeg.git -a dreamteamzurich 
heroku buildpacks:add --index 1 heroku/python -a dreamteamzurich 
```

To push use command line from the root directory:

```
git subtree push --prefix audio_analyzer heroku main
```