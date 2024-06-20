from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tgju.service.profiles_service import ProfilesService


class ProfilesScraper(BaseScraper):
    def process_data(self, json_data):
        data = json_data.get("current", [])

        if data:

            profilesService = ProfilesService()

            if not profilesService.table_exists():
                profilesService.create_table()

            profile = {}
            for element in data.keys():
                profile["Symbol"] = element
                profilesService.update_tgju_profile(profile)

            self.logger.info("Tgju profiles list retrieved successfully.")
        else:
            self.logger.warning("Tgju profiles list could not be retrieved.")
