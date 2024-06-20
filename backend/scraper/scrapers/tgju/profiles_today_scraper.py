from datetime import datetime

from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tgju.service.profiles_today_service import ProfilesTodayService


class ProfilesTodayScraper(BaseScraper):
    def process_data(self, json_data):
        data = json_data.get("data", [])

        if data:

            profilesTodayService = ProfilesTodayService()

            if not profilesTodayService.table_exists():
                profilesTodayService.create_table()

            url = list(self.data.keys())[0]
            tgju_symbol = url[url.rfind("/") + 1:]

            for element in data:
                element.insert(0, datetime.today().strftime('%Y/%m/%d'))
                element.insert(0, tgju_symbol)
                profilesTodayService.update_profile_today(self.convert_values_to_float(element))

            self.logger.info("Tgju profiles list retrieved successfully.")
        else:
            self.logger.warning("Tgju profiles list could not be retrieved.")
