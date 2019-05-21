import logging
import configparser
import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(__name__)


# Spotify config file parsing
try:
    config = configparser.ConfigParser()
    user_config_dir = os.path.expanduser("~/.config/ypc/")
    config.read(user_config_dir + 'config.ini')
    id = config['spotify']['id']
    secret = config['spotify']['secret']
except Exception as e:
    logger.error("Error with the config file. Be sure to have a valid config.ini file. \n%s", e)
    exit()

# Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=id, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_spotify_playlist_tracks(username, playlist_id):
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
        list_songs = get_spotify_playlist_tracks("spotify", playlist)
        for song in list_songs:
            artist = (str(song['track']['artists'][0]['name']))
            title = (str(song['track']['name']))
            df = df.append({"title": artist + ' - ' + title, "playlist_url": playlist}, ignore_index=True)
    # title need to be the first column
    df = df[['title', 'playlist_url']]
    return df
