from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.get_trade_service import GetTradeService


class GetTradeScraper(BaseScraper):
    def process_data(self, json_data):
        get_trade_data = json_data.get("trade", [])

        if get_trade_data:
            get_trade_service = GetTradeService()

            if not get_trade_service.table_exists():
                get_trade_service.create_table()
                self.logger.info("Created table: tse_get_trade")
            inscode = self.url.split('/')[-1]
            for msg in get_trade_data:
                msg['insCode'] = inscode
                msg['id'] = inscode + "+" + str(msg['nTran'])
                get_trade_service.update_get_trade(msg)

            self.logger.info("Prepared Data retrieved successfully.")
        else:
            self.logger.warning("GetTrade could not be retrieved.")
