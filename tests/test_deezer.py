from ypc import deezer_utils
import pandas as pd

DEEZER_FILE = "tests/test_files/deezer_urls.txt"
DEEZER_URL = "https://www.deezer.com/fr/playlist/1914526462"


def test_get_deezer_playlist_tracks():
    if not isinstance(
        deezer_utils.get_deezer_playlist_tracks(DEEZER_URL), list
    ):
        raise AssertionError()


def test_get_deezer_playlists():
    if not isinstance(
        deezer_utils.get_deezer_playlists([DEEZER_URL, DEEZER_URL]),
        pd.DataFrame,
    ):
        raise AssertionError()
