from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_group_service import InstrumentGroupService


class StaticDataScraper(BaseScraper):
    def process_data(self, json_data):
        static_data = json_data.get("staticData", [])

        if static_data:
            instrument_group_service = InstrumentGroupService()

            if not instrument_group_service.table_exists():
                instrument_group_service.create_table()
                self.logger.info("Created table: tse_instrument_groups")

            for element in static_data:
                element['name'] = element.get('name').strip()
                element['description'] = element.get('description').replace("\'", "").strip()
                instrument_group_service.update_instrument_group(element)

            self.logger.info("Static data retrieved successfully.")
        else:
            self.logger.warning("Static data could not be retrieved.")
