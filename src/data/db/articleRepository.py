from data.db.db import Base, get_engine, get_session
from data.article import Article


def initialize_db():
    Base.metadata.create_all(get_engine())
    get_engine()
    get_session()


def save(article):
    get_session().add(article)
    get_session().commit()


def save_all(articles):
    get_session().add_all(articles)
    get_session().commit()


def find_by_name_and_publication(name, publication):
    return get_session().query(Article).filter_by(name=name, publication=publication).first()


def contains_article(article):
    return find_by_name_and_publication(article.name, article.publication) is not None


def find_all_by_publication(publication):
    return get_session().query(Article).filter_by(publication=publication)


def all_articles():
    return get_session().query(Article).all()


def find_all_by_category(category):
    return get_session().query(Article).filter_by(category=category)
