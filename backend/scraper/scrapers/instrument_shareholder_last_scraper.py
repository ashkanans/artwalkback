from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_shareholder_last_service import InstrumentShareholderLastService


class InstrumentShareholderLastScraper(BaseScraper):
    def process_data(self, json_data):
        instrument_shareholder_data = json_data.get("instrumentShareholderLast", [])

        if instrument_shareholder_data:
            ins_code = instrument_shareholder_data[0].get('insCode', '')
            table_name = f"tse_inst_{ins_code}_shareholder"
            self.logger.info(f"Table name: {table_name}")

            instrument_shareholder_last_service = InstrumentShareholderLastService(table_name)

            if not instrument_shareholder_last_service.table_exists():
                instrument_shareholder_last_service.create_table()
                self.logger.info(f"Created table: {table_name}")

            for element in instrument_shareholder_data:
                instrument_shareholder_last_service.update_instrument_shareholder_last(element)

            self.logger.info("Instrument shareholder last data retrieved successfully.")
        else:
            self.logger.warning("Instrument shareholder last data could not be retrieved.")
