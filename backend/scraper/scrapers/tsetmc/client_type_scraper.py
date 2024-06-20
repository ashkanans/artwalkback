from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.client_type_service import ClientTypeService


class ClientTypeScraper(BaseScraper):
    def process_data(self, json_data):
        client_type_data = json_data.get("clientType", [])

        if client_type_data:
            client_type_service = ClientTypeService()

            if not client_type_service.table_exists():
                client_type_service.create_table()
                self.logger.info("Created table: tse_client_type")

            inscode = self.url.split('/')[-3]
            client_type_data['insCode'] = inscode
            client_type_service.update_client_type(client_type_data)

            self.logger.info("ClientType data retrieved successfully.")
        else:
            self.logger.warning("ClientType data could not be retrieved.")
