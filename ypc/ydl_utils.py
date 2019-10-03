import logging
from youtube_dl import YoutubeDL

logger = logging.getLogger(__name__)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def ydl_download(url, only_audio=False):
    try:
        if only_audio:
            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
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
    except Exception as e:
        logger.error("Error with getting the youtube url for %s : %s.", url, e)
        return None


def ydl_get_url(search_term):
    try:
        ydl_opts = {"logger": MyLogger()}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(
                f"ytsearch1:{search_term}", download=False
            )
        return info_dict["entries"][0]["webpage_url"]
    except Exception as e:
        logger.error(
            "Error with getting the youtube url for %s : %s.", search_term, e
        )
        return None
