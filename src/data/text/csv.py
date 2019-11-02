from data.article import Article
from os import linesep
from config.config import csv_target_file
from os.path import exists
# csv_format = publication!$!author"!$!"name!$!category!$!subcategory!$!text


def write_to_file(target_file, articles, mode):
    f = open(target_file, mode)
    f.write(linesep.join([str(article) for article in articles]).encode("utf-8"))
    f.write(linesep.encode("utf-8"))
    f.flush()
    f.close()


def write_to_db_file(articles):
    write_to_file(csv_target_file, articles, 'ab')


read_cache = None


def clear_cache():
    global read_cache
    read_cache = None


def read_from_csv_file():

    global read_cache
    if read_cache is not None:
        return read_cache

    articles = []

    if not exists(csv_target_file):
        return []

    f = open(csv_target_file, 'rb')
    for line in f:

        line = line.decode("utf-8")
        if line.strip() == "":
            continue

        fields = line.split("!$!")
        article = Article()
        article.publication = fields[0]
        article.author = fields[1]
        article.name = fields[2]
        article.category = fields[3]
        article.subcategory = fields[4]
        article.text = fields[5].rstrip()
        articles.append(article)

    f.close()
    read_chache = articles
    return articles

