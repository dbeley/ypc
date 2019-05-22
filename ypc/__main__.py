import argparse
import logging
import os
import time
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from .download_video import downloading_video
from .spotify_playlist import get_spotipy, get_spotify_playlists
from .deezer_playlist import get_deezer_playlists
from .youtube_extract import youtube_extract_urls

logger = logging.getLogger()
FORMAT = '%(levelname)s :: %(message)s'
temps_debut = time.time()


def parse_main_argument(argument, export_folder):
    # File or string
    if os.path.isfile(argument):
        is_file = True
        argument_file_content = open(argument).read()
        # File of urls or search terms
        is_spotify = "spotify" in argument_file_content and argument_file_content.startswith("http")
        is_deezer = "deezer" in argument_file_content and argument_file_content.startswith("http")
    else:
        is_file = False
        is_spotify = "spotify" in argument
        is_deezer = "deezer" in argument
    # get df
    if is_spotify:
        sp = get_spotipy()
        if is_file:
            with open(argument) as f:
                urls = [line.strip() for line in f]
        else:
            urls = [x.strip() for x in argument.split(',')]
        logger.debug("urls : %s.", urls)
        logger.debug("Function get_spotify_playlists.")
        df = get_spotify_playlists(sp, urls)
        logger.debug("Exporting spotify playlists to export_spotify_track_names.csv.")
        df.to_csv(export_folder + '/export_spotify_track_names.csv', index=False, sep='\t')
    elif is_deezer:
        if is_file:
            with open(argument) as f:
                urls = [line.strip() for line in f]
        else:
            urls = [x.strip() for x in argument.split(',')]
        logger.debug("urls : %s.", urls)
        logger.debug("Function get_deezer_playlists.")
        df = get_deezer_playlists(urls)
        logger.debug("Exporting deezer playlists to export_deezer_track_names.csv.")
        df.to_csv(export_folder + '/export_deezer_track_names.csv', index=False, sep='\t')
    else:
        if is_file:
            df = pd.read_csv(argument, sep='\t', header=None)
        else:
            df = pd.DataFrame([x.strip() for x in argument.split(',')])
    logger.debug(df)
    return df


def main():
    args = parse_args()

    # Export folder
    if args.export_folder_name:
        export_folder = args.export_folder_name
    else:
        export_folder = "Exports"
    logger.debug("Export folder : %s.", export_folder)
    Path(export_folder).mkdir(parents=True, exist_ok=True)

    # Parse main argument
    if args.main_argument:
        df = parse_main_argument(args.main_argument, export_folder)
    # Parse other arguments
    elif not any([args.spotify_url, args.deezer_url, args.file_name,
                  args.spotify_file, args.deezer_file]):
        logger.error('No input. Use the -h flag to see help. Exiting.')
        exit()

    # Spotify arguments
    elif args.spotify_url or args.spotify_file:
        sp = get_spotipy()
        if args.spotify_url:
            urls = [x.strip() for x in args.spotify_url.split(',')]
        if args.spotify_file:
            with open(args.spotify_file) as f:
                urls = [line.strip() for line in f]
        logger.debug("urls : %s.", urls)
        logger.debug("Function get_spotify_playlists.")
        df = get_spotify_playlists(sp, urls)
        logger.debug("Exporting spotify playlists to export_spotify_track_names.csv.")
        df.to_csv(export_folder + '/export_spotify_track_names.csv', index=False, sep='\t')
    # Deezer arguments
    elif args.deezer_url or args.deezer_file:
        if args.deezer_url:
            urls = [x.strip() for x in args.deezer_url.split(',')]
        if args.deezer_file:
            with open(args.deezer_file) as f:
                urls = [line.strip() for line in f]
        logger.debug("urls : %s.", urls)
        logger.debug("Function get_deezer_playlists.")
        df = get_deezer_playlists(urls)
        logger.debug("Exporting deezer playlists to export_deezer_track_names.csv.")
        df.to_csv(export_folder + '/export_deezer_track_names.csv', index=False, sep='\t')
    # List of search terms
    elif args.file_name:
        df = pd.read_csv(args.file_name, sep='\t', header=None)
    else:
        logger.error("Unexpected error. Use -h to see available options.")
        exit()

    if args.no_search_youtube:
        logger.info("no_search_youtube mode. Exiting.")
        exit()
    list_urls = youtube_extract_urls(df)

    logger.info("Exporting urls list.")
    with open(export_folder + '/url_list_simple.csv', 'w') as f:
        for i in list_urls:
            f.write(f"{i}\n")

    df['url'] = pd.Series(list_urls).values
    df.to_csv(export_folder + '/url_list_detailed.csv', index=False, sep='\t')

    original_folder = os.getcwd()
    # Video download
    if args.download_video:
        Path(export_folder + "/Video").mkdir(parents=True, exist_ok=True)
        os.chdir(export_folder + "/Video")
        logger.info("Downloading videos.")
        for index, row in tqdm(df.iterrows(), dynamic_ncols=True, total=df.shape[0]):
            logger.debug("Downloading video for %s : %s.", row[0], row['url'])
            downloading_video(row['url'])
        os.chdir(original_folder)
    # Audio download
    if args.download_audio:
        Path(export_folder + "/Audio").mkdir(parents=True, exist_ok=True)
        os.chdir(export_folder + "/Audio")
        logger.info("Downloading audio files.")
        for index, row in tqdm(df.iterrows(), dynamic_ncols=True, total=df.shape[0]):
            logger.debug("Downloading audio for %s : %s.", row[0], row['url'])
            downloading_video(row['url'], only_audio=True)
        os.chdir(original_folder)
    logger.info("Runtime : %.2f seconds." % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Convert spotify/deezer/text playlists to youtube urls or audio/video files.')
    parser.add_argument("main_argument", type=str, help="Any search terms allowed : search terms or deezer/spotify playlists urls (separated by comma) or filename containing search terms or deezer/spotify playlists urls (one by line)")
    parser.add_argument('--debug', help="Display debugging information.", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-f', '--file_name', type=str, help="File containing the name of the songs (one search term by line).")
    parser.add_argument('-su', '--spotify_url', type=str, help="Url of the spotify playlists (separated by comma).")
    parser.add_argument('-du', '--deezer_url', type=str, help="Url of the deezer playlists (separated by comma).")
    parser.add_argument('-sf', '--spotify_file', type=str, help="File containing the links of the spotify playlists (one by line).")
    parser.add_argument('-df', '--deezer_file', type=str, help="File containing the links of the deezer playlists (one by line).")
    parser.add_argument('-n', '--export_folder_name', type=str, help="Name of the export. Used to name the exports folder.")
    parser.add_argument('-v', '--download_video', help="Download the videos of the tracks found.", dest='download_video', action='store_true')
    parser.add_argument('-a', '--download_audio', help="Download the audio files of the tracks found.", dest='download_audio', action='store_true')
    parser.add_argument('--no_search_youtube', help="Doesn't search youtube urls. Use it with the -su/-du/-sf/-df flags if you want to export only the track names from playlists.", dest='no_search_youtube', action='store_true')
    parser.set_defaults(download_video=False, download_audio=False, no_search_youtube=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=FORMAT)
    return args


if __name__ == "__main__":
    main()
