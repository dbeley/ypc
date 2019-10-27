from threading import Thread
import logging
from youtube_dl import YoutubeDL
from tqdm import tqdm

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
                self.ydl_download(row["url"])
            except Exception as e:
                logger.error(
                    "Error downloading %s in thread %s : %s.",
                    row["url"],
                    self.num,
                    e,
                )

    def ydl_download(self, url):  # pragma: no cover
        if url:
            if self.only_audio:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "256",
                        }
                    ],
                    "logger": MyLogger(),
                    "outtmpl": "%(title)s.%(ext)s",
                }
            else:
                ydl_opts = {
                    "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                    "logger": MyLogger(),
                    "outtmpl": "%(title)s.%(ext)s",
                }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=True)
        else:
            logger.warning("Url invalid : %s. Skipping.", url)


def ydl_get_url(search_term, position):
    ydl_opts = {"logger": MyLogger()}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(
            f"ytsearch{position}:{search_term}", download=False
        )
    return info_dict["entries"][position - 1]["webpage_url"]


def get_youtube_url(search):
    position = 1
    while True:
        try:
            url = ydl_get_url(search, position)
            break
        except Exception as e:
            logger.error(
                "Error extracting url for search %s, position %s : %s.",
                search,
                position,
                e,
            )
            if position > 3:
                url = None
                break
        position += 1
    return url


class MyLogger(object):  # pragma: no cover
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
