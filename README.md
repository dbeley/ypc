# ypc : youtube_playlist_converter

This script allows the conversion of spotify/deezer/text playlists to youtube urls or audio/video files.

It supports spotify and deezer playlist urls, as well as a list of text to search (see below for an example).

If you want to extract spotify playlists, you need to set up a valid config.ini file with your spotify api client id and secret and place it in ~/.config/ypc/.

## Requirements

- valid config.ini for spotify in ~/.config/ypc/ (see config_sample.ini for an example)

## Installation in a virtualenv

```
pipenv install '-e .'
```

## Usage

### Help

```
pipenv run ypc -h
```

### Example

#### With a spotify url

Download the audio of a spotify playlist :

```
pipenv run ypc -su SPOTIFY_PLAYLIST_URL -a
```

#### With a deezer url

Download the video founds on youtube for a list of deezer playlists (one by line) :

```
pipenv run ypc -fd deezer_list_playlists.txt -v
```

#### With a csv file

Given a file sample_file.csv :

```
artist1 - title1
artist1 - title2
artist2 - title1
any search term
```

Download the audio files for the tracks/search terms in the sample csv file above :

```
pipenv run ypc -f sample_file.csv -a
```

Download the video files for the tracks/search terms in the sample csv file above :

```
pipenv run ypc -f sample_file.csv -v
```
