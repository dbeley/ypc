from threading import Thread
import logging
from youtube_dl import YoutubeDL
from tqdm import tqdm
from ypc.tag_utils import get_metadata

logger = logging.getLogger(__name__)


class YdlDownloadThread(Thread):
    def __init__(self, num, rows, only_audio=False):
        Thread.__init__(self)
        self.num = num
        self.rows = rows
        self.only_audio = only_audio
        logger.debug("Init thread %s.", self.num)

    def run(self):
        for index, row in tqdm(
            self.rows.iterrows(),
            dynamic_ncols=True,
            total=self.rows.shape[0],
            position=self.num,
        ):
            logger.debug(
                "Thread %s : Downloading %s - %s.", self.num, index, row["url"]
            )
            try:
                self.ydl_download(row)
            except Exception as e:
                logger.error(
                    "Error downloading %s in thread %s : %s.",
                    row["url"],
                    self.num,
                    e,
                )

    def ydl_download(self, row):  # pragma: no cover
        ydl_opts_base = {
            "logger": MyLogger(),
            "outtmpl": "%(title)s.%(ext)s",
            "prefer_ffmpeg": True,
            "download_archive": "ypc_progress.txt",
        }
        if not row.empty:
            metadata = None
            if "title" in row:
                metadata = get_metadata(row["title"])
            if self.only_audio:
                ydl_opts = {
                    **ydl_opts_base,
                    "writethumbnail": True,
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "256",
                        },
                        {"key": "EmbedThumbnail"},
                    ],
                }
                if metadata:
                    ydl_opts = {
                        **ydl_opts,
                        "postprocessor_args": [
                            "-metadata",
                            f"artist={metadata.artist_name}",
                            "-metadata",
                            f"title={metadata.track_name}",
                        ],
                    }
            else:
                ydl_opts = {
                    **ydl_opts_base,
                    "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                    # Would need to recode in mp4 or m4a. Useless for now.
                    # "writethumbnail": True,
                    # "postprocessors": [{"key": "EmbedThumbnail"}],
                }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(row["url"], download=True)
        else:
            logger.warning("Url invalid : %s. Skipping.", row["url"])


def dict_is_song(info_dict):
    """ Determine if a dictionary returned by youtube_dl is from a song (and not an album for example). """
    if "full album" in info_dict["title"].lower():
        return False
    if int(info_dict["duration"]) > 7200:
        return False
    return True


def get_ydl_dict(search_term, position):
    ydl_opts = {"logger": MyLogger()}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(
            f"ytsearch{position}:{search_term}", download=False
        )
    return info_dict["entries"][position - 1]


def get_youtube_url(search_term):
    """ Extract an url for a song. """
    position = 1
    while True:
        try:
            info_dict = get_ydl_dict(search_term, position)
            if dict_is_song(info_dict):
                break
        except Exception as e:
            logger.error(
                "Error extracting youtube search %s, position %s : %s.",
                search_term,
                position,
                e,
            )
            if position > 4:
                # Too many wrong results
                return None
        position += 1
    return info_dict["webpage_url"]


class MyLogger(object):  # pragma: no cover
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
