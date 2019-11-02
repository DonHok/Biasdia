from data.db.db import Base, get_engine, get_session
from data.article import Article
from config.config import use_database
from data.text.csv import write_to_db_file, read_from_csv_file, clear_cache


def initialize_db():
    if use_database:
        Base.metadata.create_all(get_engine())
        get_engine()
        get_session()


def close():
    if use_database:
        get_session().close()
    else:
        clear_cache()


def save(article):
    if use_database:
        if not contains_article(article):
            get_session()
            get_session().add(article)
            get_session().commit()
    else:
        write_to_db_file([article])


def save_all(articles):
    if use_database:
        get_session().add_all(articles)
        get_session().commit()
    else:
        write_to_db_file(articles)


def find_by_name_and_publication(name, publication):
    if use_database:
        return get_session().query(Article).filter_by(name=name, publication=publication).first()
    else:
        raise NotImplementedError


def contains_article(article):
    if use_database:
        return find_by_name_and_publication(article.name, article.publication) is not None
    else:
        raise NotImplementedError


def find_all_by_publication(publication):
    if use_database:
        return get_session().query(Article).filter_by(publication=publication)
    else:
        raise NotImplementedError


def all_articles():
    if use_database:
        return get_session().query(Article).all()
    else:
        return read_from_csv_file()


def find_all_by_category(category):
    if use_database:
        return get_session().query(Article).filter_by(category=category)
    else:
        return list(filter(lambda article: article.category == category, read_from_csv_file()))


def find_all_by_subcategory(category):
    if use_database:
        return get_session().query(Article).filter_by(subcategory=category)
    else:
        return list(filter(lambda article: article.subcategory == category, read_from_csv_file()))

