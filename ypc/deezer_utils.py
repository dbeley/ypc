import requests
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def get_deezer_playlist_tracks(playlist):
    df = pd.DataFrame()
    playlist = (
        f"https://api.deezer.com/playlist/{playlist.split('/')[-1]}/tracks"
    )
    list_res = []
    logger.debug("Playlist api url : %s", playlist)
    res = requests.get(playlist).json()
    list_res.append(res)
    while "next" in res:
        logger.debug("next tracks in playlist : %s", res["next"])
        res = requests.get(res["next"]).json()
        list_res.append(res)
        if "next" not in res:
            break
    for res in list_res:
        for track in res["data"]:
            artist = track["artist"]["name"]
            title = track["title"]
            df = df.append(
                {
                    "artist": artist,
                    "track_name": title,
                    "title": artist + " - " + title,
                    "playlist_url": playlist,
                },
                ignore_index=True,
            )
    return df


def get_deezer_album_tracks(album):
    df = pd.DataFrame()
    api_url = f"https://api.deezer.com/album/{album.split('/')[-1]}"
    logger.debug("Album api url : %s", api_url)
    res = requests.get(api_url).json()
    logger.debug("Album deezer %s : %s.", album, res)
    for track in res["tracks"]["data"]:
        artist = track["artist"]["name"]
        title = track["title"]
        df = df.append(
            {
                "artist": artist,
                "track_name": title,
                "album": res["title"],
                "album_url": album,
                "title": artist + " - " + title,
            },
            ignore_index=True,
        )
    return df


def get_deezer_songs(terms):
    df = pd.DataFrame()
    for item in terms:
        logger.debug(item)
        # item is album
        if "album" in item:
            df = pd.concat([df, get_deezer_album_tracks(item)], sort=False)
        # item is playlist
        elif "playlist" in item:
            df = pd.concat([df, get_deezer_playlist_tracks(item)], sort=False)
        else:
            logger.error(
                "%s not supported. Please retry with another search.", item
            )
            raise SystemExit
    return df
