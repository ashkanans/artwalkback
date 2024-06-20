from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.get_related_company_service import GetRelatedCompanyService


class GetRelatedCompanyScraper(BaseScraper):
    def process_data(self, json_data):
        get_related_company_data = json_data.get("relatedCompany", [])

        if get_related_company_data:
            get_related_company_service = GetRelatedCompanyService()

            if not get_related_company_service.table_exists():
                get_related_company_service.create_table()
                self.logger.info("Created table: tse_get_related_company")

            for data in get_related_company_data:
                get_related_company_service.update_get_related_company(data['instrument'])

            self.logger.info("GetRelatedCompany data retrieved successfully.")
        else:
            self.logger.warning("GetRelatedCompany data could not be retrieved.")
