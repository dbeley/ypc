import logging
import configparser
import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(__name__)


def get_spotipy():
    # Spotify config file parsing
    user_config_dir = os.path.expanduser("~/.config/ypc/")
    try:
        config = configparser.ConfigParser()
        config.read(user_config_dir + 'config.ini')
        id = config['spotify']['id']
        secret = config['spotify']['secret']
    except Exception as e:
        logger.error("Error with the config file. Be sure to have a valid ~/.config/ypc/config.ini file if you want to use the spotify playlist extraction features. Error : %s", e)
        if not os.path.exists(user_config_dir):
            logger.info("Configuration folder not found. Creating ~/.config/ypc/.")
            os.makedirs(user_config_dir)
        if not os.path.isfile(user_config_dir + "config.ini"):
            sample_config = ("[spotify]\n"
                             "id=spotify_id_here\n"
                             "secret=spotify_secret_here\n"
                             )
            with open(user_config_dir + "config.ini", 'w') as f:
                f.write(sample_config)
            logger.info("A sample configuration file has been created at ~/.config/ypc/config.ini. Go to https://developer.spotify.com/dashboard/login to create your own spotify application.")
        exit()

    # Spotify API
    client_credentials_manager = SpotifyClientCredentials(client_id=id, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def get_spotify_playlist_tracks(sp, username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def get_spotify_playlists(sp, playlists):
    df = pd.DataFrame()
    list_songs = []
    for playlist in playlists:
        logger.info("Processing spotify playlist %s", playlist)
        try:
            list_songs = get_spotify_playlist_tracks(sp, "spotify", playlist)
        except Exception as e:
            logger.error("Error when requesting Spotify API. Be sure that your config.ini file is correct. Error : %s", e)
            exit()
        for song in list_songs:
            artist = (str(song['track']['artists'][0]['name']))
            title = (str(song['track']['name']))
            df = df.append({"title": artist + ' - ' + title, "playlist_url": playlist}, ignore_index=True)
    # title need to be the first column
    df = df[['title', 'playlist_url']]
    return df
