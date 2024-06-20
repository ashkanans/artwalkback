from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.market_overview_service import MarketOverviewService


class MarketOverviewScraper(BaseScraper):
    def process_data(self, json_data):
        market_overview_data = json_data.get("marketOverview", {})

        if market_overview_data:
            market_overview_service = MarketOverviewService()

            if not market_overview_service.table_exists():
                market_overview_service.create_table()
                self.logger.info("Created table: tse_market_overview")
            if self.url[-1] == '2':
                market_overview_data["name"] = 'فرا بورس'
            else:
                market_overview_data["name"] = 'بازار نقدی بورس'
            market_value = format(float(market_overview_data['marketValue']), '.0f')
            market_overview_data['marketValue'] = market_value
            market_overview_service.update_market_overview(market_overview_data, self.url[-1])
            self.logger.info(f"Market overview data for flow {self.url[-1]} retrieved successfully.")
        else:
            self.logger.warning(f"Market overview data for {self.config.get('name')} could not be retrieved.")
