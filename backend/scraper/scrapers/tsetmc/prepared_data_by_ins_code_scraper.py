from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.codal_announcement_service import CodalAnnouncementService


class PreparedDataByInsCodeScraper(BaseScraper):
    def process_data(self, json_data):
        codal_announcements_data = json_data.get("preparedData", [])

        if codal_announcements_data:
            ins_ids = self.config['ids'][
                self.config['urls'].index(self.config['urls'][0])]  # Assuming full_urls contains only one URL
            table_name = f"tse_inst_{ins_ids}_codal_announcements"

            codal_announcement_service = CodalAnnouncementService(table_name)

            if not codal_announcement_service.table_exists():
                codal_announcement_service.create_table()
                self.logger.info(f"Created table: {table_name}")

            for element in codal_announcements_data:
                codal_announcement_service.update_codal_announcement(element)

            self.logger.info("Codal announcements retrieved successfully.")
        else:
            self.logger.warning("Codal announcements could not be retrieved.")
