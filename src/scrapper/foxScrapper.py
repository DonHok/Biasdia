from scrapper.articleScrapper import ArticleScrapper
import re
from data.article import Article


class FoxScrapper(ArticleScrapper):

    def __init__(self):
        category_pattern = re.compile("https://www\.foxnews\.com/[a-zA-Z]+")
        sub_category_article_patter = re.compile("https://www\.foxnews\.com/([-a-zA-Z]+/)+[-a-zA-Z]+")
        super(FoxScrapper, self).__init__("https://www.foxnews.com/", [category_pattern, sub_category_article_patter])

    def next(self):
        pass

    def is_article(self, b_soup):
        body = b_soup.find('body')
        return "article" in body.attrs['class']

    def extract_article(self, b_soup):
        return Article()
