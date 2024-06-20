from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.closing_price_info_service import ClosingPriceInfoService


class ClosingPriceInfoScraper(BaseScraper):
    def process_data(self, json_data):
        closing_price_info_data = json_data.get("closingPriceInfo", [])
        closing_price_info_data.pop('instrumentState')
        if closing_price_info_data:
            closing_price_info_service = ClosingPriceInfoService()

            if not closing_price_info_service.table_exists():
                closing_price_info_service.create_table()
                self.logger.info("Created table: tse_closing_price_info")

            inscode = self.url.split('/')[-1]
            closing_price_info_data['insCode'] = inscode
            closing_price_info_service.update_closing_price_info(closing_price_info_data)

            self.logger.info("ClosingPriceInfo data retrieved successfully.")
        else:
            self.logger.warning("ClosingPriceInfo data could not be retrieved.")
