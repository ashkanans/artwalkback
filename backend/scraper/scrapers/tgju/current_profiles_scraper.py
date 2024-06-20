from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tgju.service.profiles_current_service import CurrentProfilesService
from backend.scraper.tgju.service.profiles_service import ProfilesService


class CurrentProfilesScraper(BaseScraper):
    def process_data(self, json_data):
        data = json_data.get("current", [])

        if data:

            currentProfilesService = CurrentProfilesService()
            profileService = ProfilesService()

            if not currentProfilesService.table_exists():
                currentProfilesService.create_table()

            for symbol, current in data.items():
                profile = profileService.get_by_symbol(symbol)
                current["Symbol"] = profile.Symbol
                current["t_g"] = current.get("t-g")
                current.pop("t-g")
                currentProfilesService.update_tgju_current_profile(self.convert_values_to_float(current))

            self.logger.info("Current tgju profiles list retrieved successfully.")
        else:
            self.logger.warning("Current tgju profiles list could not be retrieved.")
