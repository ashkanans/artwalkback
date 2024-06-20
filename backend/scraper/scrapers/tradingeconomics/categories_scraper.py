from bs4 import BeautifulSoup
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tradingeconomics.service.categories_service import CategoriesService

class CategoriesScraper(BaseScraper):
    def process_data(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        # nav_links = soup.find_all('a', class_='nav-link')
        nav_links = soup.find_all('ul', class_='nav-tabs')
        objects = []
        for nav_links in nav_links:
            nav_links_inside = nav_links.find_all('a')

            for link in nav_links_inside:
                link_object = {'name': link.text.strip(), 'link': link['href']}
                objects.append(link_object)

        print(objects)

        categories_service = CategoriesService()

        if objects:

            if not categories_service.table_exists():
                categories_service.create_table()
                self.logger.info("Table created")

            for element in objects:
                categories_service.update_Categories(element)
        
            self.logger.info("Categories retrieved successfully.")
        else:
            self.logger.warning("Categories could not be retrieved.")
