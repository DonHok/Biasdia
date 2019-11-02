import nltk
import contractions
import re


def split_article_sentences_tokens(article):
    article_text = article.name + " . " + article.text
    article_text = article_text.replace(u'\xa0', " ").replace("-", " ")
    sentences = nltk.tokenize.sent_tokenize(article_text, language='english')
    cleaned_sentences = [contractions.fix(s).lower() for s in [sentence for sentence in sentences]]
    tokenized_sentences_words = [[word.replace(".", "").replace("\'", "")
                                  for word in nltk.tokenize.word_tokenize(sentence)]
                                 for sentence in cleaned_sentences]
    return [list(filter(lambda word: re.match("^[^a-z]*$", word) is None, sentence)) 
            for sentence in tokenized_sentences_words]
