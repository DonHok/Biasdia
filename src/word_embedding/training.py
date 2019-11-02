import gensim
from config.config import nn_seed, use_skip_gram
from logging import info
from os import linesep


class Model:

    def __init__(self, sentences):
        self.vector_size = 100
        self.model = gensim.models.Word2Vec(sentences, min_count=3, seed=nn_seed,
                                            size=self.vector_size, sg=(1, 0)[use_skip_gram])

    def save_trained_model(self, path):
        self.model.save(path)

    def add_train(self, further_sentences):
        self.model.train(further_sentences)

    def build_bags(self, words, n):
        if n == 1:
            return [word for word in words]
        else:
            res = [bag.append(word) for bag in self.build_bags(words, (n-1)) for word in words
                   if word not in bag]
            return res

    def evaluate(self, result_file, seed_words, n_bags):
        f = None
        if result_file is not None:
            f = open(result_file, 'wb')
        for n_bag in n_bags:
            bags = self.build_bags(seed_words, n_bag)
            for bag in bags:
                most_similar_words = self.model.most_similar(positive=bag, topn=100)
                info("Most similar words to: " + str(bag) + linesep)
                info(linesep.join([x[0] + " - distance: " + str(x[1]) for x in most_similar_words]))
                if f is not None:
                    f.write(b"Most similar words to: " + str(bag).encode("utf-8") + linesep.encode("utf-8"))
                    f.write(linesep.join([x[0] + " - distance: " + str(x[1]) for x in most_similar_words])
                            .encode("utf-8"))
                    f.write(linesep.encode("utf-8"))
        if f is not None:
            f.flush()
            f.close()
