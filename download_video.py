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


def downloading_video(url, only_audio=False):
    if only_audio:
        ydl_opts = {
            'format': 'bestaudio/best',
            'logger': MyLogger(),
            }
    else:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'logger': MyLogger(),
            }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
    return filename
