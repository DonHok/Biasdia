import os

database_name = None
database_pw = None
csv_target_file = None
use_database = None
max_extractions = None

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

f = open("system.config", 'r')

for line in f:
    exec(line)

