import json
import re

import requests
from bs4 import BeautifulSoup


class TradingeconomicsAUTH():
    def __init__(self, base_url, link, config_path):
        self.BaseUrl = base_url.replace("markets.", "")
        self.Link = link
        if config_path:
            with open(config_path, 'r', encoding='utf-8') as config_file:
                self.config = json.load(config_file)

        scraper_info_list = [d for d in self.config.get('requests_urls', []) if d.get('name') == 'AuthorizationHeader']
        self.Header = scraper_info_list[0].get('header')
        self.AUTH = None
        self.Symbol = None

    def get_AUTH_and_Symbol(self):
        total_url = f"{self.BaseUrl}{self.Link}"
        response = requests.get(total_url, headers=self.Header)

        if response.status_code == 200:
            # parse the HTML response
            soup = BeautifulSoup(response.text, 'html.parser')

            # find script tag which contains TESecurify value
            script_tags = soup.find_all('script')

            # iterate over all script tags and find TESecurify values
            tesecurify = re.search(r'TESecurify = \'(.*?)\';', script_tags[0].string if script_tags[0].string else '')
            symbol = re.search(r'symbol = \'(.*?)\';', script_tags[0].string if script_tags[0].string else '')
            for script_tag in script_tags:
                symbol = re.search(r'symbol = \'(.*?)\';', script_tag.string if script_tag.string else '')
                if symbol:
                    if symbol.group(1) != "":
                        self.Symbol = symbol.group(1)
                tesecurify = re.search(r'TESecurify = \'(.*?)\';', script_tag.string if script_tag.string else '')
                if tesecurify:
                    if tesecurify.group(1) != "":
                        self.AUTH = tesecurify.group(1)
                        break
