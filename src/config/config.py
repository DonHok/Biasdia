import os

database_name = None
database_pw = None
database_port = None
csv_target_file = None
use_database = None
max_extractions = None
scrapper = None
perform_scrapping = True
select_from_categories = []
select_from_subcategories = []
nn_seed = 1
use_skip_gram = True
scrapping_delay_min = 1
scrapping_delay_max = 10
persist_training_data_file = None
learn_embeddings = True
result_file = None
seed_words = []
bags = [1]

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

f = open(os.path.join(__location__, "system.config"), 'r')

for line in f:
    exec(line)

f.close()

