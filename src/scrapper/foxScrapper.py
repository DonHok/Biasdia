from scrapper.articleScrapper import ArticleScrapper
import re
from data.article import Article


class FoxScrapper(ArticleScrapper):

    def __init__(self):
        category_pattern = re.compile("https://www\.foxnews\.com/[-a-zA-Z]+")
        sub_category_article_patter = re.compile("https://www\.foxnews\.com/([-a-zA-Z]+/)+[-0-9a-zA-Z]+")
        super(FoxScrapper, self).__init__("https://www.foxnews.com/", [category_pattern, sub_category_article_patter])

    def is_article(self, b_soup):
        body = b_soup.body
        if 'class' not in body.attrs:
            return False
        return any("article" in attr for attr in body.attrs['class'])

    def handle_forward_refs(self, ref):
        if "foxnews.com" in ref:
            return ref
        if ref.startswith("/"):
            return "https://www.foxnews.com" + ref
        else:
            return "https://www.foxnews.com/" + ref

    def extract_article(self, b_soup):
        article = Article()
        article.publication = "foxnews"
        raw_article = b_soup.find('article')
        header = raw_article.find('header', {'class': "article-header"})
        article.name = header.find('h1', {'class': 'headline'}, text=True).contents[0]
        article.author = header.find('div', {'class': 'author-byline'}).find('a', text=True).contents[0]
        eyebrow = raw_article.find("div", {'class': 'eyebrow'})
        categories = eyebrow.find('a').attrs['href']
        if categories.startswith('/category'):
            categories = categories.split("/")
            if len(categories) < 4:
                article.category = categories[2]
                article.subcategory = ""
            else:
                article.category = categories[2]
                article.subcategory = categories[-1]
        else:
            categories = categories.split("/")
            article.category = categories[1]
            article.subcategory = ""

        paragraphs = raw_article.find('div', {'class': 'article-body'}).findAll('p', recursive=False)
        texts = []
        for paragraph in paragraphs:
            text = str(paragraph)
            text = re.sub(r"<p[^>]*>(.*)</p>", r"\1", text)
            if text.startswith("<strong><a") or text.endswith("</strong></a>"):
                continue
            text = ArticleScrapper.clean_up_text(paragraph)

            assert "<" not in text
            assert ">" not in text

            if "CLICK" in text:
                continue
            texts.append(text)
        article.text = " ".join(texts)
        return article

