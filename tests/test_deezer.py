from ypc import deezer_utils
import pandas as pd
import pytest

DEEZER_FILE = "tests/test_files/deezer_urls.txt"
DEEZER_PLAYLIST_URL = "https://www.deezer.com/fr/playlist/1914526462"
DEEZER_ALBUM_URL = "https://www.deezer.com/fr/album/95467"


def test_get_deezer_playlist_tracks():
    playlist_df = deezer_utils.get_deezer_playlist_tracks(DEEZER_PLAYLIST_URL)
    if not isinstance(playlist_df, pd.DataFrame):
        raise AssertionError()

    with pytest.raises(Exception):
        deezer_utils.get_deezer_playlist_tracks(DEEZER_ALBUM_URL)
        deezer_utils.get_deezer_playlist_tracks(DEEZER_FILE)


def test_get_deezer_album_tracks():
    if not isinstance(
        deezer_utils.get_deezer_album_tracks(DEEZER_ALBUM_URL), pd.DataFrame
    ):
        raise AssertionError()

    with pytest.raises(Exception):
        deezer_utils.get_deezer_album_tracks(DEEZER_PLAYLIST_URL)
        deezer_utils.get_deezer_album_tracks(DEEZER_FILE)


def test_get_deezer_songs():
    if not isinstance(
        deezer_utils.get_deezer_songs([DEEZER_PLAYLIST_URL, DEEZER_ALBUM_URL]),
        pd.DataFrame,
    ):
        raise AssertionError()
