import install
from config import config
from data.articleRepository import save, initialize_db, close, find_all_by_category, all_articles,\
    find_all_by_subcategory
from data.text.csv import write_to_file
from word_embedding.preprocessing import split_article_sentences_tokens
from word_embedding.training import Model
from os import path
import logging
import sys


def scrapping():
    f_scrapper = config.scrapper
    result = ""
    while result is not None:
        result = f_scrapper.next()
        if result is not None:
            save(result)


def load_data():
    loaded = []
    if config.select_from_categories or config.select_from_subcategories:
        for category in config.select_from_categories:
            loaded += find_all_by_category(category)
        for subcategory in config.select_from_subcategories:
            loaded += find_all_by_subcategory(subcategory)
    else:
        loaded += all_articles()
    return loaded


def persist_training_data(file, articles_to_write):
    if path.exists(file) and path.isfile(file):
        logging.warning("File " + file + " already exists. Overwriting the content with training data.")
    try:
        for to_write in articles_to_write:
            to_write.text = to_write.text.replace("\n", "")
            if to_write.subcategory is None:
                to_write.subcategory = ""
        write_to_file(file, articles_to_write, 'wb')
    except:
        logging.warning("Could not write training data to " + file)
        logging.warning("Error message: " + str(sys.exc_info()[0]))


def build_bias_words():
    articles = load_data()
    articles = list(filter(lambda art: art.text.strip() != "", articles))

    if config.persist_training_data_file is not None:
        persist_training_data(config.persist_training_data_file, articles)

    logging.info("Starting tokenizing the input.")
    sentences = []
    for article in articles:
        sentences += split_article_sentences_tokens(article)
    logging.info("Finished tokenizing the input.")
    logging.info(str(len(sentences)) + " sentences loaded.")

    model = Model(sentences)
    model.evaluate(config.result_file, config.seed_words, config.bags)


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
initialize_db()

if config.perform_scrapping:
    logging.info("Starting the scrapping process.")
    scrapping()
    logging.info("Finished the scrapping process.")

if config.learn_embeddings:
    build_bias_words()

close()
