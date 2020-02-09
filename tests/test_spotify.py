from ypc import spotify_utils
import pandas as pd
import pytest

SPOTIFY_FILE = "tests/test_files/spotify_urls.txt"
SPOTIFY_PLAYLIST_URL = (
    "https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL"
)
SPOTIFY_ALBUM_URL = "https://open.spotify.com/album/4FCoFSNIFhK36holxHWCnc"


def test_get_spotify_playlist_tracks(sp):
    if not isinstance(
        spotify_utils.get_spotify_playlist_tracks(sp, SPOTIFY_PLAYLIST_URL),
        pd.DataFrame,
    ):
        raise AssertionError()
    with pytest.raises(Exception):
        spotify_utils.get_spotify_playlist_tracks(sp, SPOTIFY_ALBUM_URL)
        spotify_utils.get_spotify_playlist_tracks(sp, SPOTIFY_FILE)


def test_get_spotify_album_tracks(sp):
    if not isinstance(
        spotify_utils.get_spotify_album_tracks(sp, SPOTIFY_ALBUM_URL),
        pd.DataFrame,
    ):
        raise AssertionError()
    with pytest.raises(Exception):
        spotify_utils.get_spotify_album_tracks(sp, SPOTIFY_PLAYLIST_URL)
        spotify_utils.get_spotify_album_tracks(sp, SPOTIFY_FILE)


def test_get_spotify_songs():
    if not isinstance(
        spotify_utils.get_spotify_songs(
            [SPOTIFY_PLAYLIST_URL, SPOTIFY_ALBUM_URL]
        ),
        pd.DataFrame,
    ):
        raise AssertionError()
