from backend.scraper.fipiran.service.indexes_id_service import IndexesIdService
from backend.scraper.scrapers.base_scraper import BaseScraper


def extract_nameFa_and_intId(string):
    row_dict = {}
    if "-" in string:
        parts = string.split("-")
        if len(parts) >= 2:
            row_dict["NameFa"] = parts[1].strip()
            row_dict["IntId"] = parts[0].strip()
        elif len(parts) == 1:
            row_dict["NameFa"] = parts[0].strip()
            row_dict["IntId"] = ""
    else:
        row_dict["NameFa"] = string.strip()
        row_dict["IntId"] = ""
    return row_dict["NameFa"], row_dict["IntId"]


class FipiranIndexesScraper(BaseScraper):
    def process_data(self, json_data):
        # #### # Data convert


        fipiran_indexes_info_data = json_data

        if fipiran_indexes_info_data:
            fipiran_indexes_info_service = IndexesIdService()

            if not fipiran_indexes_info_service.table_exists():
                fipiran_indexes_info_service.create_table()
                self.logger.info("Created table: fipiran_indexes_id")

            for row_dict in fipiran_indexes_info_data:
                row_dict["NameFa"], row_dict["IntId"] = extract_nameFa_and_intId(row_dict.get('LVal30'))

                fipiran_indexes_info_service.update_indexes_id(row_dict)


            self.logger.info("fipiran indexes id info retrieved successfully.")
        else:
            self.logger.warning("fipiran indexes id info could not be retrieved.")
