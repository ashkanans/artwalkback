from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService


class InstrumentInfoScraper(BaseScraper):
    def process_data(self, json_data):
        instrument_info_data = json_data.get("instrumentInfo", [])

        if instrument_info_data:
            instrument_info_service = InstrumentInfoService()

            if not instrument_info_service.table_exists():
                instrument_info_service.create_table()
                self.logger.info("Created table: tse_instrument_info")

            instrument_info_service.update_instrument_info(instrument_info_data)

            self.logger.info("Instrument info retrieved successfully.")
        else:
            self.logger.warning("Instrument info could not be retrieved.")
