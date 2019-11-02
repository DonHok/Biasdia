import urllib3
from bs4 import BeautifulSoup
from config.config import max_extractions, scrapping_delay_min, scrapping_delay_max
from logging import warning
from os import linesep
from time import sleep
from random import randrange
from logging import info
import sys


class ArticleScrapper:

    def __init__(self, base_url, search_url_patterns):
        self.__url_stack__ = []
        self.search_url_patterns = search_url_patterns
        self.extracted_articles = 0
        self.pool_man = urllib3.PoolManager(1)
        self.already_visited = set()
        self.initialize_stack(base_url)

    def get_page(self, url):
        response = self.pool_man.request("GET", url)
        if not response.status == 200:
            info("Could not reach page: " + url)
            sleep(randrange(1, 61, 1))
            return None
        return response

    def extract_urls(self, bsoup):
        all_hrefs = bsoup.findAll('a')

        for href in set(all_hrefs):
            if "href" not in href.attrs:
                continue

            cleaned_href = href.attrs["href"]
            cleaned_href = self.handle_forward_refs(cleaned_href)
            if not cleaned_href.startswith("https:") and not cleaned_href.startswith("http:"):
                cleaned_href = "https:" + cleaned_href
            if any(pattern.fullmatch(cleaned_href) is not None for pattern in self.search_url_patterns):
                self.__url_stack__.append(cleaned_href)

    def handle_forward_refs(self, ref):
        raise NotImplementedError

    def initialize_stack(self, base_url):
        response = self.get_page(base_url)
        if response is None:
            raise RuntimeError("Could not reach page")
        bsoup = BeautifulSoup(response.data, 'html.parser')
        self.extract_urls(bsoup)

    def is_article(self, b_soup):
        raise NotImplementedError

    def extract_article(self, b_soup):
        raise NotImplementedError

    def next(self):
        if self.__url_stack__ and self.extracted_articles < max_extractions:
            url = self.__url_stack__.pop(0)

            while url in self.already_visited and self.__url_stack__:
                url = self.__url_stack__.pop(0)

            if url in self.already_visited:
                return None

            self.already_visited.add(url)
            response = self.get_page(url)

            if response is None:
                warning("Could not get response from: " + url)
                return self.next()

            bsoup = BeautifulSoup(response.data, 'html.parser')
            self.extract_urls(bsoup)

            if self.is_article(bsoup):

                sleep(randrange(scrapping_delay_min, scrapping_delay_max, 1))
                self.extracted_articles += 1

                try:
                    return self.extract_article(bsoup)
                except:
                    warning("Exception while trying to extract url: " + url + linesep)
                    warning("Error message: " + str(sys.exc_info()[0]))
                    return None
            else:
                return self.next()
        else:
            return None

    @staticmethod
    def clean_up_text(paragraph):
        return ''.join(paragraph.findAll(text=True))

    def has_next(self):
        return len(self.__url_stack__) > 0
