import argparse
import logging
import os
import time
import pandas as pd
from pathlib import Path
from .download_video import downloading_video
from .spotify_playlist import get_spotify_playlists
from .deezer_playlist import get_deezer_playlists
from .youtube_extract import youtube_extract_urls

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()

    # Export folder
    if args.export_folder_name:
        export_folder = args.export_folder_name
    else:
        export_folder = "Exports"
    logger.debug("Export folder : %s", export_folder)
    Path(export_folder).mkdir(parents=True, exist_ok=True)

    # Check input
    if not any([args.spotify_url, args.deezer_url, args.file_name,
               args.spotify_file, args.deezer_file]):
        logger.error('No input. Use the -h flag to see help. Exiting.')
        exit()

    # Spotify
    elif args.spotify_url or args.spotify_file:
        if args.spotify_url:
            urls = [x.strip() for x in args.spotify_url.split(',')]
        if args.spotify_file:
            with open(args.spotify_file) as f:
                urls = [line.strip() for line in f]
        logger.debug("urls : %s", urls)
        logger.debug("get_spotify_playlists")
        df = get_spotify_playlists(urls)
        logger.debug("Exporting spotify playlists to export_spotify_track_names.csv")
        df.to_csv(export_folder + '/export_spotify_track_names.csv', index=False, sep='\t')
    # Deezer
    elif args.deezer_url or args.deezer_file:
        if args.deezer_url:
            urls = [x.strip() for x in args.deezer_url.split(',')]
        if args.deezer_file:
            with open(args.deezer_file) as f:
                urls = [line.strip() for line in f]
        logger.debug("urls : %s", urls)
        logger.debug("get_deezer_playlists")
        df = get_deezer_playlists(urls)
        logger.debug("Exporting deezer playlists to export_deezer_track_names.csv")
        df.to_csv(export_folder + '/export_deezer_track_names.csv', index=False, sep='\t')
    # List of search terms
    else:
        df = pd.read_csv(args.file_name, sep='\t', header=None)

    if args.no_search_youtube:
        logger.info("no_search_youtube mode. Exiting")
        exit()
    list_urls = youtube_extract_urls(df)

    logger.info("Exporting urls list")
    with open(export_folder + '/url_list_simple.csv', 'w') as f:
        for i in list_urls:
            f.write(f"{i}\n")

    df['url'] = pd.Series(list_urls).values
    df.to_csv(export_folder + '/url_list_detailed.csv', index=False, sep='\t')

    original_folder = os.getcwd()
    # Video download
    if args.download_video:
        logger.info("Downloading videos")
        Path(export_folder + "/Video").mkdir(parents=True, exist_ok=True)
        os.chdir(export_folder + "/Video")
        for index, row in df.iterrows():
            logger.info("Downloading video for %s : %s", row[0], row['url'])
            downloading_video(row['url'])
        os.chdir(original_folder)
    # Audio download
    if args.download_audio:
        logger.info("Downloading audio files")
        Path(export_folder + "/Audio").mkdir(parents=True, exist_ok=True)
        os.chdir(export_folder + "/Audio")
        for index, row in df.iterrows():
            logger.info("Downloading audio for %s : %s", row[0], row['url'])
            downloading_video(row['url'], only_audio=True)
        os.chdir(original_folder)
    logger.info("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Convert spotify/deezer/text playlists to youtube urls or audio/video files')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-f', '--file_name', type=str, help="File containing the name of the songs (one search term by line)")
    parser.add_argument('-su', '--spotify_url', type=str, help="Url of the spotify playlists (separated by comma)")
    parser.add_argument('-du', '--deezer_url', type=str, help="Url of the deezer playlists (separated by comma)")
    parser.add_argument('-sf', '--spotify_file', type=str, help="File containing the links of the spotify playlists (one by line)")
    parser.add_argument('-df', '--deezer_file', type=str, help="File containing the links of the deezer playlists (one by line)")
    parser.add_argument('-n', '--export_folder_name', type=str, help="Name of the export. Used to name the exports folder")
    parser.add_argument('-v', '--download_video', help="Download the videos of the tracks found", dest='download_video', action='store_true')
    parser.add_argument('-a', '--download_audio', help="Download the audio files of the tracks found", dest='download_audio', action='store_true')
    parser.add_argument('--no_search_youtube', help="Doesn't search youtube urls. Use it with the -u or the -s flag if you want to export only the track names from spotify playlists", dest='no_search_youtube', action='store_true')
    parser.set_defaults(download_video=False, download_audio=False, no_search_youtube=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
