# HackZurich2021

## Deploying audio_analyzer to heroku

Remeber to add the Aptfile buildpack:

```
heroku buildpacks:add --index 1 heroku/python -a dreamteamzurich 
heroku buildpacks:add --index 1 heroku-community/apt -a dreamteamzurich 
```

To push use command line from the root directory:

```
git subtree push --prefix audio_analyzer heroku main
```