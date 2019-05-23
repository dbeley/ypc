# ypc : youtube_playlist_converter

This python utility allows the conversion of spotify/deezer/text playlists to youtube urls or audio/video files.

It supports spotify and deezer playlist urls, as well as a list of terms to search (see below for some examples). 

It also supports files containing spotify or deezer playlist urls or terms to search (one by line). Unfortunately, the mix of several types is not supported at this moment (spotify and deezer playlists urls in the same file for example).

If you want to extract spotify playlists, you need to set up a valid config.ini file with your spotify api client id and secret (go to https://developer.spotify.com/dashboard/login to create your own spotify application) and place it in the ~/.config/ypc/ directory (see the config_sample.ini file as an example).

## Installation

```
pip install ypc
```

If you are an Archlinux user, you can install the AUR package [ypc-git](https://aur.archlinux.org/packages/ypc-git).

## Installation in a virtualenv

```
git clone https://github.com/dbeley/ypc
cd ypc
pipenv install '-e .'
```

## Usage

### Help

Use ypc with the -h flag to see all the available options :

```
ypc -h
```

### Examples

#### Simple Examples

Download audio files for several songs :

```
ypc "u2 one,xtc general and majors,debussy la mer" -a
```

Download videos for several deezer playlists using the name "deezer_export" as export folder :

```
ypc DEEZER_PLAYLIST_URL1,DEEZER_PLAYLIST_URL2 -v -n deezer_export
```

Download audio and video for each spotify playlists in the file spotify_playlists.txt (one by line) using the name "spotify_export" as export folder :

```
ypc spotify_playlists.txt -a -v -n spotify_export
```

The main ypc arguments you want are -a (download audio), -v (download video) and -n (set the name of the export folder).

You can set the medias (an url, a list of search terms, a file containing spotify playlist urls, etc.) to download without any argument and ypc will guess which kind of media it is, or use explicit argument, as shown in the examples below.

#### With a spotify url

Download the audio of a spotify playlist :

```
ypc SPOTIFY_PLAYLIST_URL -a
ypc -su SPOTIFY_PLAYLIST_URL -a
```

Download the video founds on youtube from a file containing spotify playlists (one by line) :

```
ypc spotify_list_playlists.txt -v
ypc -sf spotify_list_playlists.txt -v
```

#### With a deezer url

Download videos for several deezer playlists using the name "deezer_export" as export folder :

```
ypc DEEZER_PLAYLIST_URL1,DEEZER_PLAYLIST_URL2 -v -n deezer_export
ypc -du DEEZER_PLAYLIST_URL1,DEEZER_PLAYLIST_URL2 -v -n deezer_export
```

Download the video founds on youtube from a file containing deezer playlists (one by line) :

```
ypc deezer_list_playlists.txt -v
ypc -df deezer_list_playlists.txt -v
```

#### With search terms

Download audio files for several songs (no explicit argument available) :

```
ypc "u2 one,xtc general and majors,debussy la mer" -a
```

Given a file sample_file.csv :

```
artist1 - title1
artist1 - title2
artist2 - title1
any search term
```

Download the audio files for the tracks/search terms in the sample csv file above :

```
ypc sample_file.csv -a
ypc -f sample_file.csv -a
```

Download the video files for the tracks/search terms in the sample csv file above :

```
ypc sample_file.csv -v
ypc -f sample_file.csv -v
```
