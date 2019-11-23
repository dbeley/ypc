import logging
import itunespy

logger = logging.getLogger(__name__)


def get_metadata(title: str):
    try:
        return itunespy.search_track(title)[0]
    except Exception as e:
        logger.error("Error finding tags for %s : %s.", title, e)
        return None
