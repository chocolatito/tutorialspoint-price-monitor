import argparse
from src.scraper import Scraper
from src.db_manager import DBManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--create_tables", default="false", help="boolean: [true, false]")
    args = parser.parse_args()
    if args.create_tables == "true":
        DBManager.create_database()
    scraper = Scraper()
    scraper.main()
