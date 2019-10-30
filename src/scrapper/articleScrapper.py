import urllib3
from bs4 import BeautifulSoup
from config.config import max_extractions


class ArticleScrapper:

    def __init__(self, base_url, search_url_patterns):
        self.__url_stack__ = []
        self.pool_man = urllib3.PoolManager()
        self.search_url_patterns = search_url_patterns
        self.extracted_articles = 0
        self.already_visited = set()
        self.initialize_stack(base_url)

    def get_page(self, url):
        response = self.pool_man.request("GET", url)
        assert response.status == 200
        return response

    def extract_urls(self, bsoup):
        all_hrefs = bsoup.findAll('a')

        for href in set(all_hrefs):
            cleaned_href = href.attrs["href"]
            if any(pattern.fullmatch(cleaned_href) is not None for pattern in self.search_url_patterns):
                self.__url_stack__.append(cleaned_href)

    def initialize_stack(self, base_url):
        response = self.get_page(base_url)
        bsoup = BeautifulSoup(response.data, 'html.parser')
        self.extract_urls(bsoup)

    def is_article(self, b_soup):
        raise NotImplementedError

    def extract_article(self, b_soup):
        raise NotImplementedError

    def next(self):
        if self.__url_stack__ and self.extracted_articles < max_extractions:
            url = self.__url_stack__.pop(0)

            if url in self.already_visited:
                return self.next()

            response = self.get_page(url)
            bsoup = BeautifulSoup(response.data, 'html.parser')
            self.extract_urls(bsoup)

            if not self.is_article(bsoup):
                self.extracted_articles += 1
                self.already_visited.add(url)
                return self.extract_article(bsoup)
            else:
                return self.next()
        else:
            return None

    def has_next(self):
        return len(self.__url_stack__) > 0
