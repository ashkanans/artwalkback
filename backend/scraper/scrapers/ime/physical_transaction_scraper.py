import json

from backend.scraper.ime.service.physical_transaction_service import PhysicalTransactionService
from backend.scraper.scrapers.base_scraper import BaseScraper


class PhysicalTransactionScraper(BaseScraper):
    def process_data(self, json_data):
        physical_transaction_info_data = json_data.get("d", [])
        physical_transaction_info_data = json.loads(physical_transaction_info_data)
        if physical_transaction_info_data:
            physical_transaction_info_service = PhysicalTransactionService()

            if not physical_transaction_info_service.table_exists():
                physical_transaction_info_service.create_table()
                self.logger.info("Created table: ime_physical_transaction_info")

            physical_transaction_info_service.update_physical_transaction_info(physical_transaction_info_data)

            self.logger.info("physical transaction groups info retrieved successfully.")
        else:
            self.logger.warning("physical transaction groups info could not be retrieved.")
