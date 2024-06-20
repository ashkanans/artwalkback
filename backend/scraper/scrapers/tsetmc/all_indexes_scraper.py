from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.all_indexes_service import AllIndexesService


class AllIndexesScraper(BaseScraper):
    def process_data(self, json_data):
        all_indexes_data = json_data.get("indexB1", {})

        if all_indexes_data:
            all_indexes_service = AllIndexesService()

            if not all_indexes_service.table_exists():
                all_indexes_service.create_table()
                self.logger.info("Created table: tse_all_indexes")

            for row in all_indexes_data:
                row['marketName'] = self.config.get('MarketName')
                all_indexes_service.update_all_indexes(row)

            self.logger.info(f"Selected Indexes data for {self.config.get('MarketName')} retrieved successfully.")
        else:
            self.logger.warning(f"Selected Indexes data for {self.config.get('MarketName')} could not be retrieved.")
