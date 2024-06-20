import json

from backend.scraper.ime.service.producer_groups_service import ProducerGroupsService
from backend.scraper.scrapers.base_scraper import BaseScraper


class ProducerGroupsScraper(BaseScraper):
    def process_data(self, json_data):
        producer_groups_info_data = json_data.get("d", [])
        producer_groups_info_data = json.loads(producer_groups_info_data)
        if producer_groups_info_data:
            producer_groups_info_service = ProducerGroupsService()

            if not producer_groups_info_service.table_exists():
                producer_groups_info_service.create_table()
                self.logger.info("Created table: ime_producer_groups_info")

            producer_groups_info_service.update_producer_groups_info(producer_groups_info_data)

            self.logger.info("producer groups info retrieved successfully.")
        else:
            self.logger.warning("producer groups info could not be retrieved.")
