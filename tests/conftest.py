from ypc import spotify_utils
import pytest


@pytest.fixture
def sp():
    return spotify_utils.get_spotipy()
