import requests
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def get_deezer_playlist_tracks(playlist):
    playlist = f"https://api.deezer.com/playlist/{playlist.split('/')[-1]}/tracks"
    list_res = []
    res = requests.get(playlist).json()
    list_res.append(res)
    while 'next' in res:
        res = requests.get(res['next']).json()
        list_res.append(res)
        if 'next' not in res:
            break

    list_dict_tracks = []
    for res in list_res:
        for track in res['data']:
            dict_track = {'artist': track['artist']['name'],
                          'title': track['title']
                          }
            list_dict_tracks.append(dict_track)
    return list_dict_tracks


def get_deezer_playlists(playlists):
    df = pd.DataFrame()
    list_songs = []
    for playlist in playlists:
        logger.info("Processing deezer playlist %s", playlist)
        list_songs = get_deezer_playlist_tracks(playlist)
        for song in list_songs:
            df = df.append({"title": song['artist'] + ' - ' + song['title'], "playlist_url": playlist}, ignore_index=True)
    # title need to be the first column
    df = df[['title', 'playlist_url']]
    return df
