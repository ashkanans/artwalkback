from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_state_top_service import InstrumentStateTopService


class InstrumentStateTopScraper(BaseScraper):
    def process_data(self, json_data):
        instrument_state_top_data = json_data.get("instrumentState", [])

        if instrument_state_top_data:
            instrument_state_top_service = InstrumentStateTopService()

            if not instrument_state_top_service.table_exists():
                instrument_state_top_service.create_table()
                self.logger.info("Created table: tse_instrument_state_top")
            for msg in instrument_state_top_data:
                instrument_state_top_service.update_instrument_state_top(msg)

            self.logger.info("InstrumentStateTop data retrieved successfully.")
        else:
            self.logger.warning("InstrumentStateTop data could not be retrieved.")
