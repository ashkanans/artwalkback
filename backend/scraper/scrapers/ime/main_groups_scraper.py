import json

from backend.scraper.ime.service.main_groups_service import MainGroupsService
from backend.scraper.scrapers.base_scraper import BaseScraper


class MainGroupsScraper(BaseScraper):
    def process_data(self, json_data):
        # convert json_data str to dict or list

        main_groups_info_data = json_data.get("d", [])
        main_groups_info_data = json.loads(main_groups_info_data)
        if main_groups_info_data:
            main_groups_info_service = MainGroupsService()

            if not main_groups_info_service.table_exists():
                main_groups_info_service.create_table()
                self.logger.info("Created table: ime_main_groups_info")

            main_groups_info_service.update_main_groups_info(main_groups_info_data)

            self.logger.info("main groups info retrieved successfully.")
        else:
            self.logger.warning("main groups info could not be retrieved.")
