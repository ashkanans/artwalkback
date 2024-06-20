import pandas as pd
from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDate

from backend.scraper.fipiran.service.index_service import IndexService
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


class FipiranScraper(BaseScraper):
    def process_data(self, html_data):
        # #### # Data convert

        # Parse the HTML
        soup = BeautifulSoup(html_data.content, 'html.parser')

        # Find the table
        table = soup.find('table')

        if table:
            # Read the table into a DataFrame
            df = pd.read_html(str(table), header=0)[0]

            # Convert the DataFrame into a dictionary
            fipiran_info_data = df.to_dict(orient='records')

            for row_dict in fipiran_info_data:
                row_dict['nameFa'], row_dict['intId'] = extract_nameFa_and_intId(
                    self.config.get('postParams')[self.url_index].get('indexpara'))
                row_dict['instrumentID'] = self.config.get('postParams')[self.url_index].get('inscodeindex')

                persian_date_str = row_dict.get('dateissue')

                year = int(str(persian_date_str)[:4])
                month = int(str(persian_date_str)[4:6])
                day = int(str(persian_date_str)[6:8])

                # Convert Persian date to JalaliDate object
                jalali_date = JalaliDate(year, month, day)

                # Convert Persian date to Gregorian date
                gregorian_date = jalali_date.to_gregorian().strftime('%Y-%m-%d')

                # Convert Persian date to Solar date
                solar_date = jalali_date.strftime('%Y-%m-%d')

                row_dict['gregorian_date'] = gregorian_date

                row_dict['solar_date'] = solar_date

                del row_dict['name']
                row_dict['value'] = row_dict.pop('Value')

            if fipiran_info_data:
                fipiran_info_service = IndexService()

                if not fipiran_info_service.table_exists():
                    fipiran_info_service.create_table()
                    self.logger.info("Created table: fipiran_indexes")

                for row_dict in fipiran_info_data:
                    fipiran_info_service.update_index(row_dict)

                self.logger.info("fipiran indexes info retrieved successfully.")
            else:
                self.logger.warning("fipiran indexes info could not be retrieved.")
        else:
            self.logger.warning("No tables found")
