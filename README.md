# ypc : youtube_playlist_converter

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8007d6fb15334ef485aadd64e133aa97)](https://app.codacy.com/app/dbeley/ypc?utm_source=github.com&utm_medium=referral&utm_content=dbeley/ypc&utm_campaign=Badge_Grade_Dashboard)

This python utility allows the conversion of spotify/deezer/text playlists to youtube urls or audio/video files.

It supports spotify and deezer playlist urls, as well as a list of terms to search (see below for some examples). 

It also supports files containing spotify or deezer playlist urls or terms to search (one by line). Unfortunately, the mix of several types is not supported at this moment (spotify and deezer playlists urls in the same file for example).

If you want to extract spotify playlists, you need to set up a valid config.ini file with your spotify api client id and secret (go to [developer.spotify.com/dashboard/login](https://developer.spotify.com/dashboard/login) to create your own spotify application) and place it in the ~/.config/ypc/ directory (see the config_sample.ini file as an example).

## Requirements

- requests
- spotipy
- pandas
- beautifulsoup4
- youtube-dl
- lxml
- tqdm

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

Show the help :

```
ypc -h
```

```
usage: ypc [-h] [--debug] [-f FILE_NAME] [-su SPOTIFY_URL] [-du DEEZER_URL]
           [-sf SPOTIFY_FILE] [-df DEEZER_FILE] [-n EXPORT_FOLDER_NAME] [-v]
           [-a] [--no_search_youtube]
           main_argument

Convert spotify/deezer/text playlists to youtube urls or audio/video files.

positional arguments:
  main_argument         Any search terms allowed : search terms or
                        deezer/spotify playlists urls (separated by comma) or
                        filename containing search terms or deezer/spotify
                        playlists urls (one by line)

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information.
  -f FILE_NAME, --file_name FILE_NAME
                        File containing the name of the songs (one search term
                        by line).
  -su SPOTIFY_URL, --spotify_url SPOTIFY_URL
                        Url of the spotify playlists (separated by comma).
  -du DEEZER_URL, --deezer_url DEEZER_URL
                        Url of the deezer playlists (separated by comma).
  -sf SPOTIFY_FILE, --spotify_file SPOTIFY_FILE
                        File containing the links of the spotify playlists
                        (one by line).
  -df DEEZER_FILE, --deezer_file DEEZER_FILE
                        File containing the links of the deezer playlists (one
                        by line).
  -n EXPORT_FOLDER_NAME, --export_folder_name EXPORT_FOLDER_NAME
                        Name of the export. Used to name the exports folder.
  -v, --download_video  Download the videos of the tracks found.
  -a, --download_audio  Download the audio files of the tracks found.
  --no_search_youtube   Doesn't search youtube urls. Use it with the
                        -su/-du/-sf/-df flags if you want to export only the
                        track names from playlists.
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
