from ypc import __main__ as ypc
import pandas as pd
import argparse

SEARCH_FILE = "tests/test_files/search_terms.txt"
DEEZER_FILE = "tests/test_files/deezer_urls.txt"
SPOTIFY_FILE = "tests/test_files/spotify_urls.txt"
YOUTUBE_FILE = "tests/test_files/youtube_urls.txt"


def test_extract_terms_from_file():
    if ypc.extract_terms_from_file("tests/test_files/search_terms.txt") != [
        "xtc - making plans for nigel",
        "can - vitamin c",
        "david bowie - heroes",
    ]:
        raise AssertionError()


def test_extract_terms_from_arg():
    if ypc.extract_terms_from_arg("term1, term2,term3") != [
        "term1",
        "term2",
        "term3",
    ]:
        raise AssertionError()


def test_main_youtube_is_youtube():
    if ypc.main_argument_is_youtube(SEARCH_FILE):
        raise AssertionError()
    if ypc.main_argument_is_youtube(DEEZER_FILE):
        raise AssertionError()
    if ypc.main_argument_is_youtube(SPOTIFY_FILE):
        raise AssertionError()
    if not ypc.main_argument_is_youtube(YOUTUBE_FILE):
        raise AssertionError()


def test_parse_main_argument():
    args_search = argparse.Namespace(
        spotify_url=None,
        spotify_file=None,
        deezer_url=None,
        deezer_file=None,
        youtube_file=None,
        file_name=SEARCH_FILE,
    )
    args_deezer = argparse.Namespace(
        spotify_url=None,
        spotify_file=None,
        deezer_url=None,
        deezer_file=DEEZER_FILE,
        youtube_file=None,
        file_name=None,
    )
    args_spotify = argparse.Namespace(
        spotify_url=None,
        spotify_file=SPOTIFY_FILE,
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
    if not isinstance(
        ypc.parse_arguments(args_search, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_arguments(args_deezer, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_arguments(args_spotify, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
    if not isinstance(
        ypc.parse_arguments(args_youtube, "ypc_export"), pd.DataFrame
    ):
        raise AssertionError()
