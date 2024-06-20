from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.prepared_data_service import PreparedDataService


class PreparedDataScraper(BaseScraper):
    def process_data(self, json_data):
        prepared_data_data = json_data.get("preparedData", [])

        if prepared_data_data:
            prepared_data_service = PreparedDataService()

            if not prepared_data_service.table_exists():
                prepared_data_service.create_table()
                self.logger.info("Created table: tse_prepared_data")
            for msg in prepared_data_data:
                prepared_data_service.update_prepared_data(msg)

            self.logger.info("Prepared Data retrieved successfully.")
        else:
            self.logger.warning("PreparedData could not be retrieved.")
