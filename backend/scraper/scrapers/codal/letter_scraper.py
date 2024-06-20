from backend.scraper.codal.service.letter_service import LetterService
from backend.scraper.scrapers.base_scraper import BaseScraper

class LetterScraper(BaseScraper):
    def process_data(self, json_data):
        letters_data = json_data.get("Letters")

        for letter in letters_data:
            letter.pop("SuperVision")

        if letters_data:
            letterService = LetterService()

            if not letterService.table_exists():
                letterService.create_table()
                self.logger.info("Created table: codal_letters")

            for row_dict in letters_data:
                letterService.update_letter(row_dict)


            self.logger.info("codal letters info retrieved successfully.")
        else:
            self.logger.warning("codal letters info could not be retrieved.")
