import time

import requests
from jdatetime import date, timedelta
from requests import RequestException

from backend.scraper.codal.service.letter_service import LetterService
from backend.scraper.fipiran.service.indexes_id_service import IndexesIdService
from backend.scraper.tgju.service.profiles_service import ProfilesService
from backend.scraper.tradingeconomics.service.categories_service import CategoriesService
from backend.scraper.tradingeconomics.service.profiles_service import ProfilesService as TradingeconomicsProfilesService
from backend.scraper.tsetmc.service.instrument_group_service import InstrumentGroupService
from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService
from backend.utils.scraper.realtimedata.utils import convert_arabic_to_persian
from backend.utils.scraper.scrapers.url_builder.tradingeconomics_auth import TradingeconomicsAUTH


class UrlBuilder:
    def __init__(self, siteName):
        self.exception_ids = []
        self.name = ""
        self.siteName = siteName
        self.url_path = ""
        self.url_constant = ""
        self.url_type = ""
        self.base_url = ""
        self.ids = []
        self.urls = None
        self.postParams = None
        self.header = None

    def create_full_url(self, request_info):
        self.name = request_info.get('name')
        self.url_path = request_info.get('url')
        self.url_constant = request_info.get('constant')
        self.url_type = request_info.get('type')
        self.base_url = request_info.get('BaseUrl')
        self.exception_ids = request_info.get('exception-ids')
        self.postParams = request_info.get('postParams')
        self.header = request_info.get('header')

        if self.url_type == "static":
            self.urls = [f"{self.base_url}{self.url_path}"]

        elif self.url_type == "id":
            if self.name == 'GetRelatedCompany':
                instrumentGroupService = InstrumentGroupService()
                self.ids = instrumentGroupService.get_all_instrument_codes()
            else:
                self.ids = self.get_ids()

            if self.exception_ids is not None:
                self.ids = [id for id in self.ids if id not in self.exception_ids]
            if len(self.ids) == 0:
                pass
            self.urls = [f"{self.base_url}{self.url_path}".format(id=id) for id in self.ids]

        elif self.url_type == "multi":
            self.ids = self.get_ids()
            self.urls = self.ids

        elif self.url_type == "constant":
            self.urls = [f"{self.base_url}{self.url_path}".format(constant=self.url_constant)]

        elif self.url_type == "fipiran":
            self.ids = self.get_ids()
            self.urls = [f"{self.base_url}{self.url_path}".format(id=id) for id in self.ids]
            request_info['postParams'] = self.ids

        elif self.url_type == "id_and_constant":
            self.ids = self.get_ids()
            if len(self.ids) == 0:
                pass
            self.urls = [f"{self.base_url}{self.url_path}".format(id=id, constant=self.url_constant) for id in self.ids]

        elif self.url_type == "codal_letters_database":
            self.ids = self.get_ids()
            if len(self.ids) == 0:
                pass
            letter_service = LetterService()
            list_of_letters_url = []

            for id in self.ids:
                letters = letter_service.get_letter_by_symbol(id)

                for letter in letters:
                    if 'گزارش فعالیت ماهانه' in letter.Title:
                        letter_url = self.base_url + letter.Url
                        list_of_letters_url.append(letter_url)
                    elif 'صورت‌های مالی' in letter.Title:
                        if letter.Title.count(')') == 1:
                            if 'تلفیقی' in letter.Title:
                                letter_url = self.base_url + letter.Url + "&sheetId=13"
                            else:
                                letter_url = self.base_url + letter.Url + "&sheetId=1"
                            list_of_letters_url.append(letter_url)
                            list_of_letters_url.append(self.base_url + letter.Url + "&sheetId=21")
                        elif letter.Title.count(')') == 2 and '(اصلاحیه)' in letter.Title:
                            if 'تلفیقی' in letter.Title:
                                letter_url = self.base_url + letter.Url + "&sheetId=13"
                            else:
                                letter_url = self.base_url + letter.Url + "&sheetId=1"
                            list_of_letters_url.append(letter_url)
                            list_of_letters_url.append(self.base_url + letter.Url + "&sheetId=21")

            self.urls = list_of_letters_url

        elif self.url_type == "cbi_inflation_database":
            cbi_urls = []
            cbi_urls.append(self.base_url + request_info.get('url'))
            self.urls = cbi_urls

        elif self.url_type == "tradingeconomics_update_profiles":
            self.ids = self.get_ids()
            if len(self.ids) == 0:
                pass
            self.urls = [f"{self.base_url}{self.url_path}".format(id=id) for id in self.ids]

        elif self.url_type == "ime" or self.url_type == "fipiran":
            self.urls = ["https://" + self.base_url + request_info.get('url')]

        elif self.url_type == "codal_letter_pg":
            self.urls = self.get_pagination_urls()

        elif self.url_type == "tsetmc_flows":
            self.ids = ["1", "2"]
            self.urls = [f"{self.base_url}{self.url_path}".format(id=id) for id in self.ids]

        elif self.url_type == "tsetmc_flow_with_constant":
            self.ids = ["1", "2"]
            self.urls = [f"{self.base_url}{self.url_path}".format(id=id, constant=self.url_constant) for id in self.ids]

        elif self.url_type == "none":
            pass

        else:
            self.urls = [f"{self.base_url}{self.url_path}"]

        return self.urls, self.ids

    def get_ids(self):
        switch = {
            "codal": self.get_codal_ids,
            "tgju": self.get_tgju_ids,
            "tsetmc": self.get_tsetmc_ids,
            "tradingeconomics": self.get_tradingeconomics_ids,
            "fipiran": self.get_fipiran_ids
        }

        get_ids_function = switch.get(self.siteName)
        return get_ids_function()

    def get_fipiran_ids(self):
        ids = []
        if self.name == "FipiranIndexes":
            instrumentGroupService = InstrumentGroupService()
            ids = instrumentGroupService.get_all_instrument_codes()
            ids = [{"id": id + "-"} for id in ids if id != ""]
        elif self.name == "Fipiran":
            indexesIdService = IndexesIdService()
            ids = indexesIdService.get_all_indexes_id()

            # Calculate shamsi dates for two days ago and today
            today = date.today()
            two_days_ago = today - timedelta(days=2)

            # Convert the dates to the required format (assuming it's YYMMDD)
            index_start = "14" + two_days_ago.strftime("%y%m%d")
            index_end = "14" + today.strftime("%y%m%d")

            ids = [{
                "indexpara": id.LVal30,
                "inscodeindex": id.InstrumentID,
                "indexStart": index_start,
                "indexEnd": index_end
            } for id in ids if id != ""]
        return ids

    def get_codal_ids(self):
        instrumentService = InstrumentInfoService()
        ids = instrumentService.get_all_persian_symbols()
        ids = [convert_arabic_to_persian(id) for id in ids if id != ""]
        return ids

    # TODO: Implement this function
    def get_tgju_ids(self):
        tgjuProfilesService = ProfilesService()
        ids = tgjuProfilesService.get_list_of_symbols()
        ids = [item for item in ids if item not in self.exception_ids]
        return ids

    def get_tsetmc_ids(self):
        instrumentInfoService = InstrumentInfoService()
        instruments = instrumentInfoService.get_all_persian_symbols()
        listA = []
        for instrument in instruments:
            listA.append(instrumentInfoService.get_instrument_info_by_persian_symbol(
                instrument.replace("ک", "ك").replace("ی", "ي")).insCode)
        return listA

    def get_pagination_urls(self):
        instrumentInfoService = InstrumentInfoService()
        lst_url = []
        symbols = instrumentInfoService.get_all_persian_symbols()
        for symbol in symbols:
            self.postParams['Symbol'] = convert_arabic_to_persian(symbol)
            # Define the maximum number of retries
            max_retries = 5

            # Initialize the number of attempts
            attempts = 0
            response = None
            while attempts < max_retries:
                try:
                    # Attempt to send the GET request
                    response = requests.get(self.base_url, params=self.postParams, headers=self.header)

                    # If the request is successful, break out of the loop
                    break
                except RequestException:
                    # If an error occurs, wait a bit before retrying
                    time.sleep(2 ** attempts)
                    attempts += 1

            if response.status_code == 200:
                json_data = response.json()
                pages = json_data.get("Page")
                if pages == 0:
                    print(f"Pages is zero for {symbol}")
                for i in range(1, pages + 1):
                    self.postParams['PageNumber'] = str(i)
                    lst_url.append(
                        self.base_url + "?" + "&".join([f"{key}={value}" for key, value in self.postParams.items()]))
            else:
                print(f"Pagination failed for {symbol}")
            print(f"Pagination sucessful for {symbol}")
        return lst_url

    def get_tradingeconomics_ids(self):
        if (self.url_type == 'id'):
            categoriesService = CategoriesService()
            ids = categoriesService.get_all_urls()
            return ids
        if (self.url_type == 'tradingeconomics_update_profiles'):
            profilesService = TradingeconomicsProfilesService()
            ids = profilesService.get_all_urls()
            return ids
        if (self.url_type == 'multi'):
            profilesService = TradingeconomicsProfilesService()
            ids = profilesService.get_all_Profiles()
            generated_urls = []
            for commodity in ids:
                template = f"{self.base_url}{self.url_path}"
                tradingeconomics_atuh = TradingeconomicsAUTH(self.base_url, commodity.link,
                                                             'configs/tradingeconomics_requests_configs.json')
                tradingeconomics_atuh.get_AUTH_and_Symbol()
                formatted_url = template.format(link=commodity.link, type=tradingeconomics_atuh.Symbol,
                                                auth=tradingeconomics_atuh.AUTH)
                generated_urls.append(formatted_url)
            return generated_urls
