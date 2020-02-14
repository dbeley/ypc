import logging

import itunespy

logger = logging.getLogger(__name__)


class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


def get_metadata(title: str):
    logger.debug("Getting metadata for %s.", title)
    try:
        # hopefully in the "artist - track" format
        if " - " in title:
            artist_name, track_name = title.split(" - ", 1)
            return Bunch(
                artist_name=artist_name.strip(), track_name=track_name.strip()
            )
        # if not, searching tags on itunes
        else:
            return itunespy.search_track(title)[0]
    except Exception as e:
        logger.error("Error finding tags for %s : %s.", title, e)
        return None
