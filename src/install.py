from pip._internal import main
import logging
import importlib.util

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
required_packages = ["psycopg2", "sqlalchemy", "urllib3", "nltk", "contractions", "beautifulsoup4"]
logging.info("Searching for required packages: " + str(required_packages))
for package in required_packages:
    logging.info("Scanning for " + package)
    result = importlib.util.find_spec(package)
    if result is None:
        logging.info("Package " + package + " is not installed.")
        logging.info("Installing " + package)
        main.main(["install", package])
    else:
        logging.info("Package " + package + " is already installed.")
