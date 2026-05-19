from lxml.html import HtmlElement

from src import constants
from src.parser_mixin import ParserMixin
from src import utils
from src.db_manager import DBManager


class Scraper(ParserMixin):
    TARGET_URL = "https://market.tutorialspoint.com/mostpopular/courses"
    XPATH_DICT = {
        "card": '//a[text()="Get Started"]/following-sibling::div/div[1]/div',
        "course_id": './input[@value]/@value',
        "attrib": './div/h3/a',
        "price": './div/h3/following-sibling::div/p/span[@data-usd]',
        "old_price": './following-sibling::s/span[@data-usd]/@data-usd',
        "profile": './/a[contains(@href, "tutorialspoint.com/profile/")]',
    }
    MATCH_KEYS = {
        "original title": "original_title",
        "datepublished": "date_published",
        "duration": "duration",
        "country": "country",
        "director": "director",
        "screenwriter": "screenwriter",
        "cast": "cast",
        "music": "music",
        "cinematography": "cinematography",
        "producer": "producer",
        "genre": "genre",
        "movie groups": "movie_groups",
        "description": "description",
        "data_movie_id": "data_movie_id"
    }

    def __init__(self) -> None:
        self.base_logger = utils.init__logger(constants.LOG_NAME)
        self.logger = utils.adapter_log(
            base_logger=self.base_logger,
            worket_id={"worker_id": "SCRAPER"})
        self.db_manager = None
        self.configure_parser()

    def _get_item(self, element: HtmlElement) -> dict:
        attrib = element.xpath(self.XPATH_DICT["attrib"])[0].attrib
        key_list = ['href', 'title', 'data-title']
        item = {k: v for k, v in attrib.items() if k in key_list}
        item["data_title"] = item.pop("data-title")
        price_els = element.xpath(self.XPATH_DICT["price"])
        item["price"] = 0.0
        item["old_price"] = None
        if price_els:
            item["price"] = float(price_els[0].attrib["data-usd"])
            old_price_elements = price_els[0].xpath(self.XPATH_DICT["old_price"])
            if old_price_elements:
                item["old_price"] = float(old_price_elements[0])
        prof_els = element.xpath(self.XPATH_DICT["profile"])
        item["profile"] = prof_els[0].text
        item["profile_url"] = prof_els[0].attrib["href"]
        item["available"] = True
        return item

    def main(self):
        tree = self.get_tree(self.TARGET_URL)
        result = {}
        elements = tree.xpath(self.XPATH_DICT["card"])
        total = len(elements)
        for index, element in enumerate(elements):
            print(f"{index}/{total}")
            course_id = element.xpath(self.XPATH_DICT["course_id"])[0]
            if course_id in result:
                continue
            try:
                item = self._get_item(element)
            except Exception as e:
                self.logger.critical(f"COULD NOT COMPLETE - _get_item(): {e}")
                return
            item["course_id"] = course_id
            result[course_id] = item
        result = list(result.values())
        self.db_manager = DBManager(base_logger=self.base_logger)
        try:
            self.db_manager.insert(result)
        except Exception as e:
            self.logger.critical(f"COULD NOT INSERT: {e}")
            utils.save_json("result.json", result)
