import sys
import os
from config import link, CITIES
from crawl import LinkCrawler, DataCrawler,ImageCrawler
from myparser import AdvertisementParser

if __name__ == '__main__':
    switch = sys.argv[1]
    if switch == 'find_links':
        crawler = LinkCrawler(CITIES,link)
        crawler.start(store=True)
    elif switch == 'extract_pages':
        crawler = DataCrawler()
        crawler.start(store=True)
    elif switch == 'images_download':
        crawler = ImageCrawler()
        crawler.start(store=True)