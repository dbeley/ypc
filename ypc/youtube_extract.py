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
