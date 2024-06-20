from bs4 import BeautifulSoup
from backend.scraper.tradingeconomics.service.profiles_service import ProfilesService
from backend.scraper.scrapers.base_scraper import BaseScraper


class ProfilesScraper(BaseScraper):

    def process_data(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        datatable_item_firsts = soup.find_all('td', class_='datatable-item-first')
        objects = []
        for datatable_item_first in datatable_item_firsts:
            links_inside_datatable_item = datatable_item_first.find_all('a')

            for link in links_inside_datatable_item:
                link_object = {'name': link.text.strip(), 'link': link['href'], 'category': self.url.split('//')[-1].split('/', 1)[1].capitalize()}
                objects.append(link_object)

        print(objects)
        profiles_service = ProfilesService()

        if objects:

            if not profiles_service.table_exists():
                profiles_service.create_table()
                self.logger.info("Table created")

            for element in objects:
                profiles_service.update_Profiles(element)

            self.logger.info("Profiles retrieved successfully.")
        else:
            self.logger.warning("Profiles could not be retrieved.")

