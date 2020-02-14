import argparse
import logging
import os
import time
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
from ypc.spotify_utils import get_spotify_songs
from ypc.deezer_utils import get_deezer_songs
from ypc.ydl_utils import YdlDownloadThread, get_youtube_url

logger = logging.getLogger()
FORMAT = "%(levelname)s :: %(message)s"
temps_debut = time.time()


def extract_terms_from_file(file):
    with open(file, "r", encoding="utf-8") as f:
        terms = [line.strip() for line in f]
    return terms


def extract_terms_from_arg(arg):
    return [x.strip() for x in arg.split(",")]


def main_argument_is_youtube(argument):
    """ True if main_argument is a youtube file."""
    if Path(argument).is_file():
        argument_file_content = open(argument).read()
        return (
            "youtu" in argument_file_content
            and argument_file_content.startswith("http")
        )
    else:
        return False


def parse_main_argument(argument, export_folder):
    """Function parsing the main_argument argument.
    Returns a dataframe containing the search terms (or the urls if main_argument is a youtube file."""
    # File or string
    if Path(argument).is_file():
        is_file = True
        argument_file_content = open(argument).read()
        # File of urls or search terms
        is_spotify = (
            "spotify" in argument_file_content
            and argument_file_content.startswith("http")
        )
        is_deezer = (
            "deezer" in argument_file_content
            and argument_file_content.startswith("http")
        )
        is_youtube = (
            "youtu" in argument_file_content
            and argument_file_content.startswith("http")
        )
    else:
        is_file = False
        is_spotify = "spotify" in argument
        is_deezer = "deezer" in argument
        # would be equivalent to argument youtube_url, doesn't exist
        is_youtube = False
    if is_spotify:
        if is_file:
            terms = extract_terms_from_file(argument)
            df = get_spotify_songs(terms)
            logger.info(
                "Reading file containing spotify urls at %s.", argument
            )
        else:
            terms = extract_terms_from_arg(argument)
            df = get_spotify_songs(terms)
            logger.info("Reading spotify urls %s.", argument)
    elif is_deezer:
        if is_file:
            terms = extract_terms_from_file(argument)
            df = get_deezer_songs(terms)
            logger.info("Reading file containing deezer urls at %s.", argument)
        else:
            terms = extract_terms_from_arg(argument)
            df = get_deezer_songs(terms)
            logger.info("Reading deezer urls %s.", argument)
    elif is_youtube:
        if is_file:
            df = pd.read_csv(argument, sep="\t", header=None, names=["url"])
            logger.info(
                "Reading file containing youtube urls at %s.", argument
            )
    else:
        if is_file:
            df = pd.read_csv(argument, sep="\t", header=None, names=["title"])
            logger.info(
                "Reading file containing search terms at %s.", argument
            )
        else:
            df = pd.DataFrame(
                [x.strip() for x in argument.split(",")], columns=["title"]
            )
            logger.info("Reading search terms %s.", argument)
    return df


def parse_arguments(args, export_folder):
    """Parse the arguments. Returns a dataframe."""
    if args.spotify_url:
        terms = extract_terms_from_arg(args.spotify_url)
        df = get_spotify_songs(terms)
        logger.info("Reading spotify urls %s.", args.spotify_url)
    elif args.spotify_file:
        terms = extract_terms_from_file(args.spotify_file)
        df = get_spotify_songs(terms)
        logger.info(
            "Reading file containing spotify urls at %s.", args.spotify_file
        )
    elif args.deezer_url:
        terms = extract_terms_from_arg(args.deezer_url)
        df = get_deezer_songs(terms)
        logger.info("Reading deezer urls %s.", args.deezer_url)
    elif args.deezer_file:
        terms = extract_terms_from_file(args.deezer_file)
        df = get_deezer_songs(terms)
        logger.info(
            "Reading file containing deezer urls at %s.", args.deezer_file
        )
    elif args.youtube_file:
        df = pd.read_csv(
            args.youtube_file, sep="\t", header=None, names=["url"]
        )
        logger.info(
            "Reading file containing youtube urls at %s.", args.youtube_file
        )
    elif args.file_name:
        df = pd.read_csv(
            args.file_name, sep="\t", header=None, names=["title"]
        )
        logger.info(
            "Reading file containing search terms at %s.", args.file_name
        )
    return df


def thread_download(df, num_threads, only_audio, export_folder):
    """ Function spawning threads to download a part of the youtube urls. """
    if only_audio:
        logger.info("Downloading audio files with %s threads.", num_threads)
    else:
        logger.info("Downloading video files with %s threads.", num_threads)

    threads = []
    original_folder = os.getcwd()
    Path(export_folder).mkdir(parents=True, exist_ok=True)
    os.chdir(export_folder)

    # youtube urls has to be in column url of df
    list_df = np.array_split(df, num_threads)
    for index, df in enumerate(list_df):
        # Create and start threads.
        t = YdlDownloadThread(index, df, only_audio)
        t.start()
        threads.append(t)

    # Join all threads.
    for t in threads:
        t.join()
    os.chdir(original_folder)


def main():  # pragma: no cover
    args = parse_args()

    # Export folder
    export_folder = args.export_folder_name
    logger.info("Export folder : %s.", export_folder)
    Path(export_folder).mkdir(parents=True, exist_ok=True)

    is_youtube = False
    # Parse main argument
    if args.main_argument:
        df = parse_main_argument(args.main_argument, export_folder)
        is_youtube = main_argument_is_youtube(args.main_argument)
        logger.debug(
            "main_argument : %s, is_youtube : %s.",
            args.main_argument,
            is_youtube,
        )
    # Verify other arguments
    elif not any(
        [
            args.spotify_url,
            args.deezer_url,
            args.file_name,
            args.spotify_file,
            args.deezer_file,
            args.youtube_file,
        ]
    ):
        logger.error("No input. Use the -h flag to see help. Exiting.")
        raise SystemExit()
    # Parse other arguments
    else:
        df = parse_arguments(args, export_folder)

    # Parse download arguments
    if not args.download_video and not args.download_audio:
        logger.info(
            "No download options selected, but the files containing the tracklist and the extracted youtube urls will still be exported. Use the flags -a to download audio, -v to download video."
        )

    # Special mode (flag --no_search_youtube) where the tracklist is exported and no downloads are made (useful to export spotify/deezer playlists as text)
    if args.no_search_youtube:
        logger.info(
            "no_search_youtube mode. Writing tracklist.csv and exiting."
        )
        df.to_csv(
            export_folder + "/tracklist.csv",
            index=False,
            sep="\t",
            header=True,
        )
        raise SystemExit

    df_previous = None
    # Check if the export folder already contains tracklist.csv from a previous export.
    if Path(export_folder + "/tracklist.csv").is_file():
        logger.info("Detected previous export. Loading file tracklist.txt.")
        df_previous = pd.read_csv(export_folder + "/tracklist.csv", sep="\t",)
        logger.debug(df_previous)

    # Extract youtube urls except if df already contains youtube urls.
    if not is_youtube and not args.youtube_file:
        logger.info("Extracting youtube urls.")
        list_urls = []
        # loop through the df, search youtube urls for each row
        for _, x in tqdm(df.iterrows(), dynamic_ncols=True, total=df.shape[0]):
            # if x["title"] is in df_previous, no need to search on youtube
            if (
                df_previous is not None
                and x["title"] in df_previous["title"].values
            ):
                url = (
                    df_previous[df_previous["title"] == x["title"]]["url"]
                    .to_string(index=False, header=False)
                    .strip()
                )
                logger.debug(
                    "url already in tracklist.csv for %s : %s.",
                    x["title"],
                    url,
                )
                list_urls.append(url)
            else:
                list_urls.append(get_youtube_url(x["title"]))

        with open(
            export_folder + "/urls_list.csv", "w", encoding="utf-8"
        ) as f:
            for i in list_urls:
                f.write(f"{i}\n")

        df["url"] = pd.Series(list_urls).values
        df.to_csv(
            export_folder + "/tracklist.csv",
            index=False,
            sep="\t",
            header=True,
        )
    # else:
    #     # Transform df containing youtube urls to be compatible with ydl_download function
    #     df.columns = ["url"]

    if args.download_audio:
        only_audio = True
        export_folder_audio = export_folder + "/Audio"
        thread_download(df, args.num_threads, only_audio, export_folder_audio)
    if args.download_video:
        only_audio = False
        export_folder_video = export_folder + "/Video"
        thread_download(df, args.num_threads, only_audio, export_folder_video)

    logger.info("Runtime : %.2f seconds." % (time.time() - temps_debut))


def parse_args():  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Convert spotify/deezer/text albums/playlists to youtube urls or audio/video files."
    )
    parser.add_argument(
        "main_argument",
        nargs="?",
        type=str,
        help="Any search terms allowed : search terms (quoted and separated by comma), deezer/spotify playlist/album urls (separated by comma) or filename containing search terms : deezer/spotify album/playlist urls (one by line) or youtube urls (one by line).",
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-f",
        "--file_name",
        type=str,
        help="File containing the name of the songs (one search term by line).",
    )
    parser.add_argument(
        "-su",
        "--spotify_url",
        type=str,
        help="Url of the spotify album/playlist urls (separated by comma).",
    )
    parser.add_argument(
        "-du",
        "--deezer_url",
        type=str,
        help="Url of the deezer album/playlist urls (separated by comma).",
    )
    parser.add_argument(
        "-sf",
        "--spotify_file",
        type=str,
        help="File containing the links of the spotify album/playlist urls (one by line).",
    )
    parser.add_argument(
        "-df",
        "--deezer_file",
        type=str,
        help="File containing the links of the deezer album/playlist urls (one by line).",
    )
    parser.add_argument(
        "-yf",
        "--youtube_file",
        type=str,
        help="File containing youtube urls (one by line). The file urls_list.csv exported by ypc is a good candidate.",
    )
    parser.add_argument(
        "-n",
        "--export_folder_name",
        type=str,
        help="Name of the export. Used to name the exports folder.",
        default="ypc_exports",
    )
    parser.add_argument(
        "-v",
        "--download_video",
        help="Download the videos of the tracks found.",
        dest="download_video",
        action="store_true",
    )
    parser.add_argument(
        "-a",
        "--download_audio",
        help="Download the audio files of the tracks found.",
        dest="download_audio",
        action="store_true",
    )
    parser.add_argument(
        "--no_search_youtube",
        help="Doesn't search youtube urls. Use it with the -su/-du/-sf/-df flags if you want to export only the track names from the albums/playlists.",
        dest="no_search_youtube",
        action="store_true",
    )
    parser.add_argument(
        "--num_threads",
        help="Number of threads to use to download the audio/video files (Default: 4, only effective if the -a/-v flags are set).",
        type=int,
        default=4,
    )
    parser.set_defaults(
        download_video=False, download_audio=False, no_search_youtube=False
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=FORMAT)
    return args


if __name__ == "__main__":
    main()
