import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def youtube_extract_urls(df):
    # Extracting youtube urls
    list_urls = []
    header = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    session = requests.Session()
    session.headers.update = header
    for index, row in df.iterrows():
        logger.info("Extracting youtube url for %s", row[0])
        url = "https://www.youtube.com/results?search_query=" + row[0].replace(' ', '+').replace('&', '%26')
        logger.debug(url)
        html = session.get(url).content
        soup = BeautifulSoup(html, 'lxml')

        try:
            titles = soup.find_all('a', {'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})
            href = [x['href'] for x in titles if x['href']]
            # delete user channels url
            href = [x for x in href if 'channel' not in x and 'user' not in x]
            logger.debug("href : %s", href)
            url = "https://www.youtube.com" + href[0]
            logger.debug(url)
            list_urls.append(url)
        except Exception as e:
            logger.error(e)
    return list_urls
