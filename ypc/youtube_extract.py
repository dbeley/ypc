# Deprecated
import requests
import logging
from bs4 import BeautifulSoup
from tqdm import tqdm

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)


def youtube_extract_urls(df):
    # Extracting youtube urls
    list_urls = []
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    session = requests.Session()
    session.headers.update = header
    logger.info("Extracting youtube urls.")
    for index, row in tqdm(
        df.iterrows(), dynamic_ncols=True, total=df.shape[0]
    ):
        url = "https://www.youtube.com/results?search_query=" + row[0].replace(
            " ", "+"
        ).replace("&", "%26")
        logger.debug(
            "%s : Extracting youtube url for %s at %s.", index, row[0], url
        )
        html = session.get(url).content
        soup = BeautifulSoup(html, "lxml")
        # Test if youtube is rate-limited
        if soup.find("form", {"id": "captcha-form"}):
            logger.error(
                "Rate-limit detected on Youtube. Exiting. Wait at east one hour before retrying."
            )
            exit()
        try:
            titles = soup.find_all(
                "a",
                {
                    "class": "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link"
                },
            )
            href = [x["href"] for x in titles if x["href"]]
            # delete user channels url
            href = [x for x in href if "channel" not in x and "user" not in x]
            logger.debug("href : %s.", href)
            url = "https://www.youtube.com" + href[0]
            list_urls.append(url)
        except Exception as e:
            logger.error(e)
    return list_urls


def get_youtube_url(search_term):
    # Extracting youtube urls
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    with requests.Session() as session:
        session.headers.update = header
        logger.debug("Extracting youtube url for %s.", search_term)
        url = "https://www.youtube.com/results?search_query=" + search_term.replace(
            " ", "+"
        ).replace(
            "&", "%26"
        ).replace(
            "(", "%28"
        ).replace(
            ")", "%29"
        )
        logger.debug("Youtube URL search : %s", url)
        soup = BeautifulSoup(session.get(url).content, "lxml")
    # Test if youtube is rate-limited
    if soup.find("form", {"id": "captcha-form"}):
        logger.error("Rate-limit detected on Youtube. Exiting.")
        return None
    try:
        titles = soup.find_all(
            "a",
            {
                "class": "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link"
            },
        )
        href = [x["href"] for x in titles if x["href"]]
        # delete user channels url
        href = [x for x in href if "channel" not in x and "user" not in x]
        id_video = href[0].split("?v=", 1)[-1]
        if "&list" in id_video:
            id_video = id_video.split("&list")[0]
        logger.debug("href : %s.", href)
        url = f"https://youtu.be/{id_video}"
    except Exception as e:
        logger.error(e)
        return None
    return url
