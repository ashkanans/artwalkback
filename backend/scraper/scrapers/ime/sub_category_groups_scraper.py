import json

from backend.scraper.ime.service.sub_category_groups_service import SubCategoryGroupsService
from backend.scraper.scrapers.base_scraper import BaseScraper


class SubCategoryGroupsScraper(BaseScraper):
    def process_data(self, json_data):
        sub_category_groups_info_data = json_data.get("d", [])
        sub_category_groups_info_data = json.loads(sub_category_groups_info_data)

        if sub_category_groups_info_data:
            sub_category_groups_info_service = SubCategoryGroupsService()

            if not sub_category_groups_info_service.table_exists():
                sub_category_groups_info_service.create_table()
                self.logger.info("Created table: ime_sub_category_groups_info")

            sub_category_groups_info_service.update_sub_category_groups_info(sub_category_groups_info_data)

            self.logger.info("sub category groups info retrieved successfully.")
        else:
            self.logger.warning("sub category groups info could not be retrieved.")
