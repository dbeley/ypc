from ypc import __main__ as ypc
import pandas as pd
import argparse
import pytest
import os

DEEZER_ALBUM_URL = "https://www.deezer.com/fr/album/95467"
DEEZER_FILE = "tests/test_files/deezer_urls.txt"
DEEZER_PLAYLIST_URL = "https://www.deezer.com/fr/playlist/1914526462"
SEARCH_FILE = "tests/test_files/search_terms.txt"
SEARCH_TERM = "xtc - making plans for nigel"
SPOTIFY_ALBUM_URL = "https://open.spotify.com/album/4FCoFSNIFhK36holxHWCnc"
SPOTIFY_FILE = "tests/test_files/spotify_urls.txt"
SPOTIFY_PLAYLIST_URL = (
    "https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL"
)
YOUTUBE_FILE = "tests/test_files/youtube_urls.txt"
YOUTUBE_URL = "https://www.youtube.com/watch?v=WfKhVV-7lxI"


def test_extract_terms_from_file():
    if ypc.extract_terms_from_file("tests/test_files/search_terms.txt") != [
        "xtc - making plans for nigel",
        "can - vitamin c",
        "david bowie - heroes",
    ]:
        raise AssertionError()

    with pytest.raises(Exception):
        ypc.extract_terms_from_file("tests/test_files/invalid.txt")


def test_extract_terms_from_arg():
    if ypc.extract_terms_from_arg("term1, term2,term3") != [
        "term1",
        "term2",
        "term3",
    ]:
        raise AssertionError()


def test_main_argument_is_youtube():
    if ypc.main_argument_is_youtube(SEARCH_FILE):
        raise AssertionError()
    if ypc.main_argument_is_youtube(DEEZER_FILE):
        raise AssertionError()
    if ypc.main_argument_is_youtube(SPOTIFY_FILE):
        raise AssertionError()
    if not ypc.main_argument_is_youtube(YOUTUBE_FILE):
        raise AssertionError()
    if ypc.main_argument_is_youtube("test"):
        raise AssertionError()


def test_parse_argument():
    args_search = argparse.Namespace(
        spotify_url=None,
        spotify_file=None,
        deezer_url=None,
        deezer_file=None,
        youtube_file=None,
        file_name=SEARCH_FILE,
    )
    args_deezer_file = argparse.Namespace(
        spotify_url=None,
        spotify_file=None,
        deezer_url=None,
        deezer_file=DEEZER_FILE,
        youtube_file=None,
        file_name=None,
    )
    args_deezer_url = argparse.Namespace(
        spotify_url=None,
        spotify_file=None,
        deezer_url=DEEZER_ALBUM_URL,
        deezer_file=None,
        youtube_file=None,
        file_name=None,
    )
    args_spotify_file = argparse.Namespace(
        spotify_url=None,
        spotify_file=SPOTIFY_FILE,
        deezer_url=None,
        deezer_file=None,
        youtube_file=None,
        file_name=None,
    )
    args_spotify_url = argparse.Namespace(
        spotify_url=SPOTIFY_ALBUM_URL,
        spotify_file=None,
        deezer_url=None,
        deezer_file=None,
        youtube_file=None,
        file_name=None,
    )
    args_youtube = argparse.Namespace(
        spotify_url=None,
        spotify_file=None,
        deezer_url=None,
        deezer_file=None,
        youtube_file=YOUTUBE_FILE,
        file_name=None,
    )
    args_no_youtube = argparse.Namespace(
        spotify_url=None,
        spotify_file=None,
        deezer_url=None,
        deezer_file=None,
        youtube_file="https://youtube.com",
        file_name=None,
    )
    if not isinstance(
        ypc.parse_arguments(args_search, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_arguments(args_deezer_file, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_arguments(args_deezer_url, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_arguments(args_spotify_file, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_arguments(args_spotify_url, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_arguments(args_youtube, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()

    with pytest.raises(Exception):
        ypc.parse_arguments("invalid", "invalid")
        ypc.parse_arguments(args_no_youtube, "ypc_export"), pd.DataFrame


def test_parse_main_argument():
    if not isinstance(
        ypc.parse_main_argument(DEEZER_ALBUM_URL, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_main_argument(DEEZER_FILE, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_main_argument(DEEZER_PLAYLIST_URL, "ypc_export"),
        pd.DataFrame,
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_main_argument(SEARCH_FILE, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_main_argument(SEARCH_TERM, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_main_argument(SPOTIFY_ALBUM_URL, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_main_argument(SPOTIFY_FILE, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_main_argument(SPOTIFY_PLAYLIST_URL, "ypc_export"),
        pd.DataFrame,
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_main_argument(YOUTUBE_FILE, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_main_argument(YOUTUBE_URL, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="doesn't work with Travis",
)
def test_parse_args():
    if not isinstance(ypc.parse_args(), argparse.Namespace):
        raise AssertionError()
