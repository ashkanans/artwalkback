from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.selected_indexes_service import SelectedIndexesService


class SelectedIndexesScraper(BaseScraper):
    def process_data(self, json_data):
        selected_indexes_data = json_data.get("indexB1", {})

        if selected_indexes_data:
            selected_indexes_service = SelectedIndexesService()

            if not selected_indexes_service.table_exists():
                selected_indexes_service.create_table()
                self.logger.info("Created table: tse_selected_indexes")

            for row in selected_indexes_data:
                selected_indexes_service.update_selected_indexes(row)

            self.logger.info(f"Selected Indexes data for {self.config.get('MarketName')} retrieved successfully.")
        else:
            self.logger.warning(f"Selected Indexes data for {self.config.get('MarketName')} could not be retrieved.")
