from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.top_trade_most_visited_service import TradeTopService


class TradeTopMostVisitedScraper(BaseScraper):
    def process_data(self, json_data):
        trade_top_data = json_data.get("tradeTop", [])

        if trade_top_data:
            trade_top_service = TradeTopService()

            if not trade_top_service.table_exists():
                trade_top_service.create_table()
                self.logger.info("Created table: tse_trade_top_most_visited")

            for element in trade_top_data:
                element.pop("instrument")
                element["marketName"] = self.config.get('name')
                trade_top_service.update_trade_top_most_visited(element)

            self.logger.info(f"Trade top data for {self.config.get('name')} retrieved successfully.")
        else:
            self.logger.warning(f"Trade top data for {self.config.get('name')} could not be retrieved.")
