from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.best_limits_service import BestLimitsService


class BestLimitsScraper(BaseScraper):
    def process_data(self, json_data):
        best_limits_data = json_data.get("bestLimits", [])

        if best_limits_data:
            best_limits_service = BestLimitsService()

            if not best_limits_service.table_exists():
                best_limits_service.create_table()
                self.logger.info("Created table: tse_best_limits")
            inscode = self.url.split('/')[-1]
            for dict in best_limits_data:
                dict['insCode'] = inscode
                dict['key'] = inscode + ' + ' + str(dict['number'])
                best_limits_service.update_best_limits(dict)

            self.logger.info("Best Limits data retrieved successfully.")
        else:
            self.logger.warning("Best Limits data could not be retrieved.")
