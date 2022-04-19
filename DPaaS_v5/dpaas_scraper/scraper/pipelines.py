# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import re
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem

from .settings import MONGO_DATABASE, MONGO_URI

from .constants import DIAPER_SIZES, DIAPERS_REGEX
import logging


REPLACEMENTS = {
    "pr": [r"prematuro"],
    "rn": [r"reci.*n nacido"],
    "huggies": [r"hugies"],
    "g": [r"grande"],
    "m": [r"s\-m"],
}

logger = logging.getLogger(__name__)

class DiaperPipeline:

    def _clean_description(self, description):
        description = description.lower()
        for value, expressions in REPLACEMENTS.items():
            for expresion in expressions:
                if re.search(expresion, description):
                    description = re.sub(expresion, value, description)
                    break
        return description

    def _extract_data(self, description):
        for expresion in DIAPERS_REGEX:
            match = re.match(expresion, description)
            if match:
                return match
        return None

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        description = adapter.get("description")
        price = adapter.get("price")
        if description and price:
            description = self._clean_description(description)
            match = self._extract_data(description)
            if not match:
                raise DropItem(f"Not a diaper - {item}")
            brand = match.group("brand")
            size = match.group("size")
            units = int(match.group("units"))
            adapter['description'] = description
            adapter['brand'] = brand
            adapter['size'] = size
            adapter['target_kg'] = DIAPER_SIZES.get(brand, {}).get(size)
            adapter['units'] = units
            adapter['unit_price'] = round(price / units, 2) if units else None
            return item
        raise DropItem(f"Missing data in {item}")


class MongoPipeline:

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        logger.info(f"MONGO_URI={MONGO_URI}, MONGO_DATABAS={MONGO_DATABASE}")
        return cls(
            mongo_uri=MONGO_URI,
            mongo_db=MONGO_DATABASE
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.collection_name].delete_many({"website": spider.allowed_domains[0]})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item