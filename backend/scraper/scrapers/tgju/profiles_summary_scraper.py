from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tgju.service.profiles_summary_service import ProfilesSummaryService


class ProfilesSummaryScraper(BaseScraper):
    def process_data(self, json_data):
        data = json_data.get("data", [])

        if data:

            profilesSummaryService = ProfilesSummaryService()

            if not profilesSummaryService.table_exists():
                profilesSummaryService.create_table()

            url = list(self.data.keys())[0]
            tgju_symbol = url[url.rfind("/") + 1:]
            for element in data:
                element.insert(0, tgju_symbol)
                profilesSummaryService.update_profile_summary(self.convert_values_to_float(element))

            self.logger.info("Tgju profiles list retrieved successfully.")
        else:
            self.logger.warning("Tgju profiles list could not be retrieved.")
