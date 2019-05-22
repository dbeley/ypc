# ypc : youtube_playlist_converter

This python utility allows the conversion of spotify/deezer/text playlists to youtube urls or audio/video files.

It supports spotify and deezer playlist urls, as well as a list of text to search (see below for an example).

If you want to extract spotify playlists, you need to set up a valid config.ini file with your spotify api client id and secret (go to https://developer.spotify.com/dashboard/login to create your own spotify application) in the ~/.config/ypc/ directory (see the config_sample.ini file as an example).

## Installation

```
pip install ypc
```

## Installation in a virtualenv

```
pipenv install '-e .'
```

## Usage

### Help

Use ypc with the -h flag to see all the available options :

```
ypc -h
```

### Example

#### With a spotify url

Download the audio of a spotify playlist :

```
ypc -su SPOTIFY_PLAYLIST_URL -a
```

#### With a deezer url

Download the video founds on youtube for a list of deezer playlists (one by line) :

```
ypc -fd deezer_list_playlists.txt -v
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
ypc -f sample_file.csv -a
```

Download the video files for the tracks/search terms in the sample csv file above :

```
ypc -f sample_file.csv -v
```
