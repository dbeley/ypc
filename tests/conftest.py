from ypc import spotify_utils
import pytest
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


@pytest.fixture
def sp():
    try:
        return spotify_utils.get_spotipy()
    except Exception as e:
        print(e)
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        )
        return spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )
