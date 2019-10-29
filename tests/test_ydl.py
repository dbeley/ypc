import pytest
import os
from ypc import ydl_utils

SEARCH_FILE = "tests/test_files/search_terms.txt"
SEARCH_TERM = "xtc - making plans for nigel"
SEARCH_TERM_IS_ALBUM = "john coltrane - my favorite things full album"
SEARCH_TERM_IS_TOO_LONG = "crab rave 10 hours"
YOUTUBE_FILE = "tests/test_files/youtube_urls.txt"
YOUTUBE_URL = "https://www.youtube.com/watch?v=WfKhVV-7lxI"


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="doesn't work with Travis",
)
def test_get_youtube_url():
    if not isinstance(ydl_utils.get_youtube_url(SEARCH_TERM), str):
        raise AssertionError()


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="doesn't work with Travis",
)
def test_get_ydl_dict():
    info_dict = ydl_utils.get_ydl_dict(SEARCH_TERM, 1)
    if not isinstance(info_dict, dict):
        raise AssertionError()

    if not ydl_utils.dict_is_song(info_dict):
        raise AssertionError()


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="doesn't work with Travis",
)
def test_dict_is_song():
    if ydl_utils.dict_is_song(ydl_utils.get_ydl_dict(SEARCH_TERM_IS_ALBUM, 1)):
        raise AssertionError()

    if ydl_utils.dict_is_song(
        ydl_utils.get_ydl_dict(SEARCH_TERM_IS_TOO_LONG, 1)
    ):
        raise AssertionError()
