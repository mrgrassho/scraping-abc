# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from asyncio.log import logger
import re
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .constants import DIAPER_SIZES, DIAPERS_REGEX

REPLACEMENTS = {
    "pr": [r"prematuro"],
    "rn": [r"reci.*n nacido"],
    "huggies": [r"hugies"],
    "g": [r"grande"],
    "m": [r"s\-m"],
}

import logging

logger = logging.getLogger(__name__)

class DiaperPipeline:
    drop_count = 0
    processed_count = 0

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
        logger.info(f"dropped items = {self.drop_count}, processed count = {self.processed_count}")
        adapter = ItemAdapter(item)
        description = adapter.get("description")
        price = adapter.get("price")
        if description and price:
            description = self._clean_description(description)
            match = self._extract_data(description)
            if not match:
                self.drop_count += 1
                raise DropItem(f"Not a diaper - {item}")
            self.processed_count += 1
            brand = match.group("brand")
            size = match.group("size")
            units = int(match.group("units"))
            adapter['description'] = description
            adapter['brand'] = brand
            adapter['size'] = size
            adapter['target_kg'] = DIAPER_SIZES.get(brand, {}).get(size)
            adapter['units'] = units
            adapter['unit_price'] = price / units if units else None
            return item
        raise DropItem(f"Missing data in {item}")
