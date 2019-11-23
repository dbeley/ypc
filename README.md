# ypc : youtube_playlist_converter

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8007d6fb15334ef485aadd64e133aa97)](https://app.codacy.com/app/dbeley/ypc?utm_source=github.com&utm_medium=referral&utm_content=dbeley/ypc&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.com/dbeley/ypc.svg?branch=master)](https://travis-ci.com/dbeley/ypc)
[![codecov](https://codecov.io/gh/dbeley/ypc/branch/master/graph/badge.svg)](https://codecov.io/gh/dbeley/ypc)

This python utility allows the conversion of spotify/deezer/text albums/playlists to youtube urls and/or audio/video files.

It supports spotify and deezer urls (album and playlist), as well as a list of terms to search (see below for some examples). 

It also supports files containing several of the compatible search terms (one by line). Unfortunately, the mix of several types is not supported at this moment (spotify and deezer urls in the same file for example).

If you want to extract spotify albums/playlists, you need to set up a valid config.ini file with your spotify api client id and secret (go to [developer.spotify.com/dashboard/login](https://developer.spotify.com/dashboard/login) to create your own spotify application) and place it in the ~/.config/ypc/ directory (see the config_sample.ini file as an example).

## Requirements

- ffmpeg
- requests
- spotipy
- pandas
- beautifulsoup4
- youtube-dl
- lxml
- tqdm
- itunespy

## Installation

```
pip install ypc
```

If you are an Archlinux user, you can install the AUR package [ypc-git](https://aur.archlinux.org/packages/ypc-git).

### Installation in a virtualenv

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
           [-sf SPOTIFY_FILE] [-df DEEZER_FILE] [-yf YOUTUBE_FILE]
           [-n EXPORT_FOLDER_NAME] [-v] [-a] [--no_search_youtube]
           [--num_threads NUM_THREADS]
           [main_argument]

Convert spotify/deezer/text albums/playlists to youtube urls or audio/video
files.

positional arguments:
  main_argument         Any search terms allowed : search terms (quoted and
                        separated by comma), deezer/spotify playlist/album
                        urls (separated by comma) or filename containing
                        search terms : deezer/spotify album/playlist urls (one
                        by line) or youtube urls (one by line).

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information.
  -f FILE_NAME, --file_name FILE_NAME
                        File containing the name of the songs (one search term
                        by line).
  -su SPOTIFY_URL, --spotify_url SPOTIFY_URL
                        Url of the spotify album/playlist urls (separated by
                        comma).
  -du DEEZER_URL, --deezer_url DEEZER_URL
                        Url of the deezer album/playlist urls (separated by
                        comma).
  -sf SPOTIFY_FILE, --spotify_file SPOTIFY_FILE
                        File containing the links of the spotify
                        album/playlist urls (one by line).
  -df DEEZER_FILE, --deezer_file DEEZER_FILE
                        File containing the links of the deezer album/playlist
                        urls (one by line).
  -yf YOUTUBE_FILE, --youtube_file YOUTUBE_FILE
                        File containing youtube urls (one by line). The file
                        url_list_simple.csv exported by ypc is a good
                        candidate.
  -n EXPORT_FOLDER_NAME, --export_folder_name EXPORT_FOLDER_NAME
                        Name of the export. Used to name the exports folder.
  -v, --download_video  Download the videos of the tracks found.
  -a, --download_audio  Download the audio files of the tracks found.
  --no_search_youtube   Doesn't search youtube urls. Use it with the
                        -su/-du/-sf/-df flags if you want to export only the
                        track names from the albums/playlists.
  --num_threads NUM_THREADS
                        Number of threads to use to download the audio/video
                        files (Default: 4, only effective if the -a/-v flags
                        are set).
```

### Examples

#### Simple Examples

Download videos for several songs :

```
ypc "u2 one,xtc general and majors,debussy la mer" -v
```

Download videos for several deezer playlists or albums using the name "deezer_export" as export folder :

```
ypc "DEEZER_PLAYLIST_URL1,DEEZER_ALBUM_URL2,..." -v -n deezer_export
```

Download audio and videos for each spotify playlists in the file spotify_playlists.txt (one by line) using the name "spotify_export" as export folder :

```
ypc spotify_playlists.txt -a -v -n spotify_export
```

The main ypc arguments you want are -a (download audio), -v (download video) and -n (set the name of the export folder, default : ypc_export).

If you don't set the `-a` and the `-v` flags, the script will still extract youtube urls for the search and write the csv files (see "Exported files").

You can set the medias (an url, a list of search terms, a file containing spotify playlist and/or album urls, etc.) to download without any argument and ypc will guess which kind of media it is (as show above), or use explicit argument, as shown in the examples below.

#### With spotify urls

Download the audio of a spotify playlist :

```
ypc SPOTIFY_PLAYLIST_URL -a
ypc -su SPOTIFY_PLAYLIST_URL -a
```

Download the videos found on youtube for the tracks of the spotify album urls contained in a file (one by line) :

```
ypc spotify_list_albums.txt -v
ypc -sf spotify_list_albums.txt -v
```

#### With deezer urls

Download videos for several deezer playlists using the name "deezer_export" as export folder :

```
ypc DEEZER_PLAYLIST_URL1,DEEZER_PLAYLIST_URL2 -v -n deezer_export
ypc -du DEEZER_PLAYLIST_URL1,DEEZER_PLAYLIST_URL2 -v -n deezer_export
```

Download the videos founds on youtube from a file containing deezer playlists (one by line) :

```
ypc deezer_list_playlists.txt -v
ypc -df deezer_list_playlists.txt -v
```

#### With youtube urls

Download the videos from a file containing youtube urls (one by line) :

```
ypc youtube_urls.txt -v
ypc -yf youtube_urls.txt -v
```

Extract youtube urls for several songs with song_export as export folder :

```
ypc "u2 one,xtc general and majors,debussy la mer" -n song_export
```

Download the videos from the exported file (works with every `urls_list.csv` exported by ypc) :

```
ypc song_export/urls_list.csv -v -n video_export
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

Download the videos for the tracks/search terms in the sample csv file above :

```
ypc sample_file.csv -v
ypc -f sample_file.csv -v
```

### Exported files

The script will export several files in the export folder (you can set it with the `-n/--export_folder_name` flag, default : ypc_export) :

- tracklist.csv : File containing the name of the songs and the youtube urls (CSV, separator : tabulation `\t`).
- urls_list.csv : File containing the list of extracted youtube urls (one by line). You can use that file with ypc (see Examples - With youtube urls)
- Audio : Folder containing the audio files (if `-a`)
- Videos : Folder containing the video files (if `-v`)
