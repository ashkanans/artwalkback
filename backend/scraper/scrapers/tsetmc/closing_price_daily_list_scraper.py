from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.closing_price_daily_list_service import ClosingPriceDailyListService


class ClosingPriceDailyListScraper(BaseScraper):
    def process_data(self, json_data):
        stock_history_data = json_data.get("closingPriceDaily", [])

        if stock_history_data:
            ins_code = stock_history_data[0].get('insCode', '')
            table_name = f"tse_inst_{ins_code}_history"
            self.logger.info(f"Table name: {table_name}")

            closing_price_daily_list_service = ClosingPriceDailyListService(table_name)

            if not closing_price_daily_list_service.table_exists():
                closing_price_daily_list_service.create_table()
                self.logger.info(f"Created table: {table_name}")

            for element in stock_history_data:
                closing_price_daily_list_service.update_closing_price_daily_list(element)

            self.logger.info("Closing price daily list retrieved successfully.")
        else:
            self.logger.warning("Closing price daily list could not be retrieved.")
