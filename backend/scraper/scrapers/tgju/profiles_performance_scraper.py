import json
import os
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tgju.service.profiles_performance_service import ProfilesPerformanceService
from backend.scraper.tgju.service.profiles_service import ProfilesService
from backend.utils.scraper.tgju.utils import find_tables_with_name


class ProfilesPerformanceScraper(BaseScraper):
    TABLE_NAME_AT_A_GLANCE = "Performance"

    def __init__(self, config):
        super().__init__(config=config)
        self.load_table_names_map()

    def load_table_names_map(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir))
        config_path = os.path.join(parent_dir, 'configs', 'tgju_profiles_names_map.json')

        with open(config_path, 'r', encoding='utf-8') as config_file:
            tgju_names_map = json.load(config_file)
            self.config['p2e_table_names_map'] = tgju_names_map.get("p2e_table_names_map").get(self.config.get('name'))

    def process_data(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')

        english_to_persian_map = {value: key for key, value in self.config.get('p2e_table_names_map').items()}

        for tables_name in self.config.get('p2e_table_names_map').values():
            table = find_tables_with_name(soup, english_to_persian_map[tables_name])

            if table and tables_name == self.TABLE_NAME_AT_A_GLANCE:
                table_body = table.find('tbody')
                rows = table_body.find_all('tr')

                cols_values = []
                for row in rows:
                    cols = row.find_all('td')
                    cols_values = [ele.text.strip() for ele in cols]

                    # Convert string numbers to double
                    for i in [1, 2, 3, 4, 5, 6]:

                        pos_sign = cols[i].find('span', {'class': 'high'})
                        if pos_sign:
                            cols_values[i] = '+' + str(cols_values[i])
                        neg_sign = cols[i].find('span', {'class': 'low'})
                        if neg_sign:
                            cols_values[i] = '-' + str(cols_values[i])

                    profiles_performance_service = ProfilesPerformanceService()
                    profiles_performance_service.create_table()

                    profiles_service = ProfilesService()

                    parsed_url = urlparse(self.url)
                    tgju_symbol = parsed_url.path.split('/')[-2]

                    cols_values.insert(0, tgju_symbol)
                    profiles_performance_service.update_performance_profile(
                        self.convert_values_to_float(cols_values))

                self.logger.debug(f"Tgju profiles retrieved successfully for table name: {tables_name}")
            else:
                self.logger.warning(f"Tgju profiles could not be retrieved for table name: {tables_name}")

    def extract_column_values(self, rows):
        values = []

        for row in rows:
            cols = row.find_all('td')
            cols_values = [ele.text.strip() for ele in cols]
            cols_values[1] = cols_values[1]

            text_left = row.find('td', {'class': 'text-left'})
            pos_sign = text_left.find('span', {'class': 'high'})
            if pos_sign:
                cols_values[1] = '+' + str(cols_values[1])
            neg_sign = text_left.find('span', {'class': 'low'})
            if neg_sign:
                cols_values[1] = '-' + str(cols_values[1])

            # Convert string numbers to double
            values.append(cols_values[1])

        return values

    def get_h1_text_content(self, soup):
        h1_tag = soup.find('h1', class_='title')
        text_content = h1_tag.text if h1_tag else ""
        return text_content
