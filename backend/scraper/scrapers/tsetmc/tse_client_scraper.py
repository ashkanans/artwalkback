import pandas as pd

from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_group_service import InstrumentGroupService
from datetime import datetime, timedelta

from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService
from backend.scraper.tsetmc.service.tse_client_instrument_and_share_service import TseClientInstrumentAndShareService
from backend.scraper.tsetmc.tsetmc_soap_services.tsetmc_service_base import *
from backend.utils.scraper.realtimedata.utils import convert_persian_to_arabic


class TseClientScraper(BaseScraper):
    def process_data(self, data):
        instrumentService = InstrumentInfoService()
        url = self.config.get('url')
        # Get instrument and share from web service
        instrument_and_share = get_instrument_and_share(0, 0)

        # process instrument_and_share and generate instrument info list
        tse_client_instrument_info = generateInstrument(instrument_and_share)

        # process instrument_and_share and generate share info list
        tse_client_share_info = generateShare(instrument_and_share)

        tse_instrument_and_share_service = TseClientInstrumentAndShareService()
        tse_instrument_and_share_service.create_tables()
        # res_instrument = tse_instrument_and_share_service.add_or_update_instrument_info(tse_client_instrument_info)
        # res_share = tse_instrument_and_share_service.add_or_update_share_info(tse_client_share_info)

        # Create a datetime object to retrieve data from the past 10 years.
        current_datetime = datetime.now()
        first_date = current_datetime - datetime(2009, 2, 15)
        new_datetime = current_datetime - timedelta(days=first_date.days)
        # Calculate adjusted price just for selected insCode
        selectedSymbols = instrumentService.get_all_persian_symbols()
        for item in selectedSymbols:
            insCode = instrumentService.get_instrument_info_by_persian_symbol(convert_persian_to_arabic(item)).insCode
            closingPrice = getInsturmentClosingPrice(insCode)
            # Calculate 2-افزایش سرمایه
            # new_closing_price_list = calculateAdjustedPrice(2, new_datetime, item.insCode, closingPrice,
            #                                                 tse_client_share_info, tse_client_instrument_info)
            # tse_instrument_and_share_service.add_or_update_closing_price_adjusted(new_closing_price_list)

            # Calculate 1-"افزایش سود و سرمایه

            new_closing_price_list = calculateAdjustedPrice(1, new_datetime, insCode, closingPrice,
                                                            tse_client_share_info, tse_client_instrument_info)

            column_names = [
                "adjustMode",
                "createdDate",
                "dEven",
                "insCode",
                "pClosing",
                "pDrCotVal",
                "pdrCotVal",
                "priceFirst",
                "priceMax",
                "priceMin",
                "priceYesterday",
                "qTotCap",
                "qTotTran5J",
                "zTotTran"
            ]
            # Convert list of objects to dictionary
            data_dict = [{col_name: getattr(obj, col_name) for col_name in column_names} for obj in
                         new_closing_price_list]

            # Convert dictionary to DataFrame
            df = pd.DataFrame(data_dict)

            # Save DataFrame to Excel
            excel_file_path = f"closing_price_info_{insCode}.xlsx"
            df.to_excel(excel_file_path, index=False)

            tse_instrument_and_share_service.add_or_update_closing_price_adjusted(new_closing_price_list)

        # Calculate adjusted price for all insCode
        # for item in tse_client_instrument_info:
        #     closingPrice = getInsturmentClosingPrice(item.insCode)
        #
        #     # Calculate 2-افزایش سرمایه
        #     # new_closing_price_list = calculateAdjustedPrice(2, new_datetime, item.insCode, closingPrice,
        #     #                                                 tse_client_share_info, tse_client_instrument_info)
        #     # tse_instrument_and_share_service.add_or_update_closing_price_adjusted(new_closing_price_list)
        #
        #     # Calculate 1-"افزایش سود و سرمایه
        #
        #     new_closing_price_list = calculateAdjustedPrice(1, new_datetime, item.insCode, closingPrice,
        #                                                     tse_client_share_info, tse_client_instrument_info)
        #     tse_instrument_and_share_service.add_or_update_closing_price_adjusted(new_closing_price_list)
