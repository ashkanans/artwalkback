import json

from backend.scraper.ime.service.category_groups_service import CategoryGroupsService
from backend.scraper.scrapers.base_scraper import BaseScraper


class CategoryGroupsScraper(BaseScraper):
    def process_data(self, json_data):
        category_groups_info_data = json_data.get("d", [])
        category_groups_info_data = json.loads(category_groups_info_data)
        if category_groups_info_data:
            category_groups_info_service = CategoryGroupsService()

            if not category_groups_info_service.table_exists():
                category_groups_info_service.create_table()
                self.logger.info("Created table: ime_category_groups_info")

            category_groups_info_service.update_category_groups_info(category_groups_info_data)

            self.logger.info("category groups info retrieved successfully.")
        else:
            self.logger.warning("category groups info could not be retrieved.")
