import os
import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service

from backend.scraper.cbi.service.inflation_rate_yearly_service import InflationRateYearlyService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.utils.string.string_utils import convert_persian_to_english_digits


class InflationRateYearlyScraper(BaseScraper):

    def __init__(self, config):
        super().__init__(config)
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def raise_event(self, data):
        for listener in self.listeners:
            listener.handle_event(data)

    def getInflationRateYearly(self, url):
        edge_options = webdriver.EdgeOptions()
        # Using headless we'll get selenium.common.exceptions.WebDriverException: Message: unknown error: net::ERR_CONNECTION_RESET
        # edge_options.add_argument("--headless")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-sh-usage")
        edge_options.add_argument("start-minimized")
        # Add this line to run Edge in headless mode
        current_path = Path.cwd().parent
        edge_driver_path = r'lib\edge_driver\msedgedriver.exe'
        edge_service = Service(os.path.join(current_path, edge_driver_path))

        driver = webdriver.Edge(service=edge_service, options=edge_options)
        driver.get(url)
        # Allow JavaScript to execute (wait for some time to load)
        driver.implicitly_wait(10)
        time.sleep(7)
        # Get the page source after JavaScript execution
        html_content = driver.page_source
        # close the Selenium webdriver
        driver.quit()

        soup = BeautifulSoup(html_content, 'html5lib')
        # Find the tables using their class attribute or any other identifying feature
        monthly_table = soup.find('table',
                                  class_='table table-hover table-responsive table-condensed table-bordered table-striped')
        annual_table = soup.find_all('table',
                                     class_='table table-hover table-responsive table-condensed table-bordered table-striped')[
            1]

        # Extract data from the monthly table
        monthly_data = []
        for row in monthly_table.find_all('tr')[1:]:
            columns = row.find_all('td')
            month = columns[0].text.strip()
            index = columns[1].text.strip()
            inflation_rate = columns[2].text.strip()
            monthly_data.append({'Month': month, 'Index': index, 'Inflation Rate': inflation_rate})

        # Extract data from the annual table
        annual_data = []
        for row in annual_table.find_all('tr')[1:]:
            columns = row.find_all('td')
            year = int(convert_persian_to_english_digits(columns[0].text.strip()))
            index = float(convert_persian_to_english_digits(columns[1].text.strip()))
            inflation_rate = float(convert_persian_to_english_digits(columns[2].text.strip()))
            annual_data.append({'Year': year, 'Index': index, 'InflationRate': inflation_rate})

        return annual_data

    def process_data(self, url):
        inflationRateYearlyService = InflationRateYearlyService()
        # self.raise_event('get inflation rate yearly started.')
        annual_data = self.getInflationRateYearly('https://www.cbi.ir/Inflation/Inflation_FA.aspx')
        # self.raise_event('get inflation rate yearly finished. saving in db started...')

        print(len(annual_data))

        tableCreationOk = inflationRateYearlyService.create_table()

        updated_years = inflationRateYearlyService.update_inflation_rate_yearly(annual_data)
        # self.raise_event('saving in db finished.')
