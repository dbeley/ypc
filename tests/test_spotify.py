from ypc import spotify_utils
import pandas as pd

# import pytest
# import os

SPOTIFY_FILE = "tests/test_files/spotify_urls.txt"
SPOTIFY_URL = "https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL"


# @pytest.mark.skipif(
#     "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
#     reason="doesn't work with Travis",
# )
def test_get_spotify_playlist_tracks(sp):
    if not isinstance(
        spotify_utils.get_spotify_playlist_tracks(sp, None, SPOTIFY_URL), list
    ):
        raise AssertionError()


# @pytest.mark.skipif(
#     "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
#     reason="doesn't work with Travis",
# )
def test_get_spotify_playlists():
    if not isinstance(
        spotify_utils.get_spotify_playlists([SPOTIFY_URL, SPOTIFY_URL]),
        pd.DataFrame,
    ):
        raise AssertionError()
