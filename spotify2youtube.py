import argparse
import logging
import configparser
import os
import time
import requests
import spotipy
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
from download_video import downloading_video

logger = logging.getLogger()
temps_debut = time.time()

# Config file parsing
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    myid = config['spotify']['id']
    mysecret = config['spotify']['secretid']
except Exception as e:
    logger.error("Error with the config file. Be sure to have a valid config.ini file. \n%s", e)
    exit()

# Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=myid, client_secret=mysecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def get_spotify_playlists(playlists):
    df = pd.DataFrame()
    list_songs = []
    for playlist in playlists:
        logger.info("Processing spotify playlist %s", playlist)
        list_songs = get_playlist_tracks("spotify", playlist)
        # with open("list_songs.csv", 'w') as f:
        #     for i in list_songs:
        #         f.write(i + '\n')
        for song in list_songs:
            artist = (str(song['track']['artists'][0]['name']))
            title = (str(song['track']['name']))
            df = df.append({"title": artist + ' - ' + title, "playlist_id": playlist}, ignore_index=True)
    return df


def main():
    args = parse_args()

    # Export folder
    if args.export_folder_name:
        export_folder = args.export_folder_name
    else:
        export_folder = "Exports"
    logger.debug("Export folder : %s", export_folder)
    Path(export_folder).mkdir(parents=True, exist_ok=True)

    # Getting list of search terms
    if not args.url and not args.file_name and not args.file_spotify_playlists:
        logger.error('No input. Use the -u or -f flag to input an url. Exiting.')
        exit()
    elif args.url or args.file_spotify_playlists:
        if args.url:
            urls = [x.strip() for x in args.url.split(',')]
        if args.file_spotify_playlists:
            with open(args.file_spotify_playlists) as f:
                urls = [line.strip() for line in f]
        logger.debug("urls : %s", urls)
        logger.debug("get_spotify_playlists")
        df = get_spotify_playlists(urls)
        logger.debug("Exporting spotify playlists to export_spotify_track_names.csv")
        df.to_csv(export_folder + '/export_spotify_track_names.csv', index=False, sep='\t')
        if args.no_search_youtube:
            logger.info("no_search_youtube mode. Exiting")
            exit()
    else:
        df = pd.read_csv(args.file_name, sep='\t')

    # Extracting youtube urls
    list_urls = []
    header = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    session = requests.Session()
    session.headers.update = header
    for index, row in df.iterrows():
        logger.info("Extracting youtube url for %s", row['title'])
        url = "https://www.youtube.com/results?search_query=" + row['title'].replace(' ', '+')
        logger.debug(url)
        html = session.get(url).content
        soup = BeautifulSoup(html, 'lxml')

        try:
            titles = soup.find_all('a', {'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})
            href = [x['href'] for x in titles if x['href']]
            # delete user channels url
            href = [x for x in href if 'channel' not in x and 'user' not in x]
            logger.debug("href : %s", href)
            url = "https://www.youtube.com" + href[0]
            logger.debug(url)
            list_urls.append(url)
        except Exception as e:
            logger.error(e)

    logger.info("Exporting urls list")
    with open(export_folder + '/url_list.csv', 'w') as f:
        for i in list_urls:
            f.write(f"{i}\n")

    df['url'] = pd.Series(list_urls).values
    df.to_csv(export_folder + '/url_list_detailed.csv', index=False, sep='\t')

    original_folder = os.getcwd()
    # Video download
    if args.download_video:
        logger.info("Downloading videos")
        Path(export_folder + "/Video").mkdir(parents=True, exist_ok=True)
        os.chdir(export_folder + "/Video")
        for index, row in df.iterrows():
            logger.info("Downloading video for %s : %s", row['title'], row['url'])
            downloading_video(row['url'])
        os.chdir(original_folder)
    # Audio download
    if args.download_audio:
        logger.info("Downloading audio files")
        Path(export_folder + "/Audio").mkdir(parents=True, exist_ok=True)
        os.chdir(export_folder + "/Audio")
        for index, row in df.iterrows():
            logger.info("Downloading audio for %s : %s", row['title'], row['url'])
            downloading_video(row['url'], only_audio=True)
        os.chdir(original_folder)
    logger.info("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Convert spotify playlist to youtube urls')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-u', '--url', type=str, help="Url of the spotify playlists (separated by comma)")
    parser.add_argument('-f', '--file_name', type=str, help="File containing the name of the songs (one search term by line)")
    parser.add_argument('-s', '--file_spotify_playlists', type=str, help="File containing the links of the spotify playlists (one by line, with 'title' as header. See example in README.md)")
    parser.add_argument('-n', '--export_folder_name', type=str, help="Name of the export. Used to name the exports folder")
    parser.add_argument('-v', '--download_video', help="Download the videos of the tracks found", dest='download_video', action='store_true')
    parser.add_argument('-a', '--download_audio', help="Download the audio files of the tracks found", dest='download_audio', action='store_true')
    parser.add_argument('--no_search_youtube', help="Doesn't search youtube urls. Use it with the -u or the -s flag if you want to export only the track names from spotify playlists", dest='no_search_youtube', action='store_true')
    parser.set_defaults(download_video=False, download_audio=False, no_search_youtube=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
