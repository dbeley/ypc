import argparse
import logging
import os
import time
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from ypc.spotify_utils import get_spotify_playlists
from ypc.deezer_utils import get_deezer_playlists
from ypc.ydl_utils import ydl_download, ydl_get_url

logger = logging.getLogger()
FORMAT = "%(levelname)s :: %(message)s"
temps_debut = time.time()


def main_argument_is_youtube(argument):
    """ True if main_argument is a youtube file."""
    if os.path.isfile(argument):
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
    if os.path.isfile(argument):
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
            df = get_spotify_playlists(terms)
            logger.info(
                "Reading file containing spotify urls at %s.", argument
            )
        else:
            terms = extract_terms_from_arg(argument)
            df = get_spotify_playlists(terms)
            logger.info("Reading spotify urls %s.", argument)
    elif is_deezer:
        if is_file:
            terms = extract_terms_from_file(argument)
            df = get_deezer_playlists(terms)
            logger.info("Reading file containing deezer urls at %s.", argument)
        else:
            terms = extract_terms_from_arg(argument)
            df = get_deezer_playlists(terms)
            logger.info("Reading deezer urls %s.", argument)
    elif is_youtube:
        if is_file:
            df = pd.read_csv(argument, sep="\t", header=None)
            logger.info(
                "Reading file containing youtube urls at %s.", argument
            )
        else:
            logger.error(
                "Unexpected error in parse_main_argument function. Exiting."
            )
            exit()
    else:
        if is_file:
            df = pd.read_csv(argument, sep="\t", header=None)
            logger.info(
                "Reading file containing search terms at %s.", argument
            )
        else:
            df = pd.DataFrame([x.strip() for x in argument.split(",")])
            logger.info("Reading search terms %s.", argument)
    return df


def parse_arguments(args, export_folder):
    """Parse the arguments. Returns a dataframe."""
    if args.spotify_url:
        terms = extract_terms_from_arg(args.spotify_url)
        df = get_spotify_playlists(terms)
        logger.info("Reading spotify urls %s.", args.spotify_url)
    elif args.spotify_file:
        terms = extract_terms_from_file(args.spotify_file)
        df = get_spotify_playlists(terms)
        logger.info(
            "Reading file containing spotify urls at %s.", args.spotify_file
        )
    elif args.deezer_url:
        terms = extract_terms_from_arg(args.deezer_url)
        df = get_deezer_playlists(terms)
        logger.info("Reading deezer urls %s.", args.deezer_url)
    elif args.deezer_file:
        terms = extract_terms_from_file(args.deezer_file)
        df = get_deezer_playlists(terms)
        logger.info(
            "Reading file containing deezer urls at %s.", args.deezer_file
        )
    elif args.youtube_file:
        # terms = extract_terms_from_file(args.youtube_file)
        df = pd.read_csv(args.youtube_file, sep="\t", header=None)
        logger.info(
            "Reading file containing youtube urls at %s.", args.youtube_file
        )
    elif args.file_name:
        # terms = extract_terms_from_file(args.file_name)
        df = pd.read_csv(args.file_name, sep="\t", header=None)
        logger.info(
            "Reading file containing search terms at %s.", args.file_name
        )
    else:
        logger.error("Unexpected error in parse_arguments function. Exiting.")
        exit()
    return df


def extract_terms_from_file(file):
    with open(file) as f:
        terms = [line.strip() for line in f]
    return terms


def extract_terms_from_arg(arg):
    return [x.strip() for x in arg.split(",")]


def main():
    args = parse_args()

    # Export folder
    if args.export_folder_name:
        export_folder = args.export_folder_name
    else:
        export_folder = "ypc_exports"
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
        exit()
    # Parse other arguments
    else:
        df = parse_arguments(args, export_folder)

    # Parse download arguments
    if not args.download_video and not args.download_audio:
        logger.info(
            "No download options selected, but the files containing the tracklist and the extracted youtube urls will still be exported. Use the flags -a to download audio, -v to download video."
        )

    if args.no_search_youtube:
        logger.info("no_search_youtube mode. Exiting.")
        df.to_csv(
            export_folder + "/tracklist.csv",
            index=False,
            sep="\t",
            header=False,
        )
        exit()

    # Extract youtube urls except if df already contains youtube urls.
    if not is_youtube and not args.youtube_file:
        logger.info("Extracting youtube urls.")
        list_urls = []
        for _, x in tqdm(df.iterrows(), dynamic_ncols=True, total=df.shape[0]):
            list_urls.append(ydl_get_url(x[0]))

        logger.info("Exporting urls list.")
        with open(export_folder + "/urls_list.csv", "w") as f:
            for i in list_urls:
                f.write(f"{i}\n")

        df["url"] = pd.Series(list_urls).values
        df.to_csv(
            export_folder + "/tracklist.csv",
            index=False,
            sep="\t",
            header=False,
        )
    else:
        # Transform df containing youtube urls to be compatible with ydl_download function
        df.columns = ["url"]

    original_folder = os.getcwd()
    # youtube urls has to be in column url of df
    # Video download
    if args.download_video:
        Path(export_folder + "/Video").mkdir(parents=True, exist_ok=True)
        os.chdir(export_folder + "/Video")
        logger.info("Downloading video files.")
        for index, row in tqdm(
            df.iterrows(), dynamic_ncols=True, total=df.shape[0]
        ):
            logger.debug("%s : Downloading video for %s.", index, row[0])
            ydl_download(row["url"])
        os.chdir(original_folder)
    # Audio download
    if args.download_audio:
        Path(export_folder + "/Audio").mkdir(parents=True, exist_ok=True)
        os.chdir(export_folder + "/Audio")
        logger.info("Downloading audio files.")
        for index, row in tqdm(
            df.iterrows(), dynamic_ncols=True, total=df.shape[0]
        ):
            logger.debug("%s : Downloading audio for %s.", index, row[0])
            ydl_download(row["url"], only_audio=True)
        os.chdir(original_folder)
    logger.info("Runtime : %.2f seconds." % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert spotify/deezer/text playlists to youtube urls or audio/video files."
    )
    parser.add_argument(
        "main_argument",
        nargs="?",
        type=str,
        help="Any search terms allowed : search terms (quoted and separated by comma), deezer/spotify playlists urls (separated by comma) or filename containing search terms, deezer/spotify playlists urls (one by line) or youtube urls (one by line).",
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
        help="Url of the spotify playlists (separated by comma).",
    )
    parser.add_argument(
        "-du",
        "--deezer_url",
        type=str,
        help="Url of the deezer playlists (separated by comma).",
    )
    parser.add_argument(
        "-sf",
        "--spotify_file",
        type=str,
        help="File containing the links of the spotify playlists (one by line).",
    )
    parser.add_argument(
        "-df",
        "--deezer_file",
        type=str,
        help="File containing the links of the deezer playlists (one by line).",
    )
    parser.add_argument(
        "-yf",
        "--youtube_file",
        type=str,
        help="File containing youtube urls (one by line). The file url_list_simple.csv exported by ypc is a good candidate.",
    )
    parser.add_argument(
        "-n",
        "--export_folder_name",
        type=str,
        help="Name of the export. Used to name the exports folder.",
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
        help="Doesn't search youtube urls. Use it with the -su/-du/-sf/-df flags if you want to export only the track names from playlists.",
        dest="no_search_youtube",
        action="store_true",
    )
    parser.set_defaults(
        download_video=False, download_audio=False, no_search_youtube=False
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=FORMAT)
    return args


if __name__ == "__main__":
    main()
