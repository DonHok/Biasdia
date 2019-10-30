from data.article import Article
from os import linesep
from config.config import csv_target_file
# csv_format = publication!$!name!$!category!$!subcategory!$!text


def write_to_file(articles):
    f = open(csv_target_file, 'a')
    f.write(linesep.join(articles))
    f.flush()
    f.close()


def read_from_csv_file():
    articles = []
    f = open(csv_target_file, 'r')

    for line in f:
        fields = line.split("!$!")
        article = Article()
        article.publication = fields[0]
        article.name = fields[1]
        article.category = fields[2]
        article.subcategory = fields[3]
        article.text = fields[4].rstrip()
        articles.append(article)

