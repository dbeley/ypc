# spotify2youtube

Script allowing the conversion of spotify playlists to youtube url list, audio files or video files.

It can also take as input a list of text to search (see below for an example) :


## Requirements

- config.ini (see config_sample.ini for an example)

## Installation of the virtualenv

```
pipenv install
```

## Usage

### Help

```
pipenv run python spotify2youtube.py -h
```

### Example

#### With a spotify url

```
pipenv run python spotify2youtube.py -u SPOTIFY_PLAYLIST_URL
```

#### With a csv file

Given a file sample_file.csv (the 'title' is mandatory) :

```
title
artist1 - title1
artist1 - title2
artist2 - title1
```

Download the audio for the tracks in the sample csv file above :

```
pipenv run python spotify2youtube.py -f sample_file.csv -a
```

Download the video for the tracks in the sample csv file above :

```
pipenv run python spotify2youtube.py -f sample_file.csv -v
```
