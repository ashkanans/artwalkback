from backend.scraper.realtimedata.service.tse_symbols_report_service import TseSymbolsReportService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.best_limits_service import BestLimitsService
from backend.scraper.tsetmc.service.client_type_service import ClientTypeService
from backend.scraper.tsetmc.service.closing_price_info_service import ClosingPriceInfoService
from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService

headers = [
    " نام نماد ",
    "خرید",
    "فروش",
    "آخرین",
    "تغییر آخرین",
    "اولین",
    "پایانی",
    "تغییر پایانی",
    "پایانی دیروز",
    "حجم",
    "ارزش معاملات",
    "ارزش بازار",
    "بازه بالای روز",
    "بازه پایین روز",
    "مجاز بالا",
    "مجاز پایین",
    "تعداد سهام",
    "حجم مبنا",
    "سهام شناور",
    "میانگین حجم ماه",
    "EPS",
    "P/E",
    "P/E GROUP",
    "P/S",
    "خرید حقیقی",
    "فروش حقیقی",
    "خرید حقوقی",
    "فروش حقوقی",
    "تعداد خریدار حقیقی",
    "تعداد فروشنده حقیقی",
    "تعداد خریدار حقوقی",
    "تعداد فروشنده حقیقی",
    "خط 1 حجم خرید",
    "خط 2 حجم خرید",
    "خط 3 حجم خرید",
    "خط 4 حجم خرید",
    "خط 5 حجم خرید",
    "خط 1 خرید",
    "خط 2 خرید",
    "خط 3 خرید",
    "خط 4 خرید",
    "خط 5 خرید",
    "خط 1 فروش",
    "خط 2 فروش",
    "خط 3 فروش",
    "خط 4 فروش",
    "خط 5 فروش",
    "خط 1 حجم فروش",
    "خط 2 حجم فروش",
    "خط 3 حجم فروش",
    "خط 4 حجم فروش",
    "خط 5 حجم فروش",
    "آخرین اطلاعات قیمت"
]


class TseSymbolsReportScraper(BaseScraper):
    def process_data(self, data):
        instrumentInfoService = InstrumentInfoService()
        persian_symbols = instrumentInfoService.get_all_persian_symbols()

        tse_symbols_report_service = TseSymbolsReportService()

        rows = [headers]

        for symbol in persian_symbols:
            insId = instrumentInfoService.get_instrument_info_by_persian_symbol(symbol).insCode
            rowdata = self.fill_row(insId)
            rowdata.insert(0, symbol)
            rows.append(rowdata)

        # First create rows and then delete the table
        tse_symbols_report_service.create_table()
        tse_symbols_report_service.delete_all_tse_symbols_report_entries()

        if rows:
            for row in rows:
                tse_symbols_report_service.update_tse_symbols_report_entry(row)

    def fill_row(self, inscode):

        # make instances

        best_limits_service = BestLimitsService()
        closing_price_info_service = ClosingPriceInfoService()
        instrument_info_Service = InstrumentInfoService()
        client_type_service = ClientTypeService()

        result = []
        # columns 2,3
        data2_3 = best_limits_service.get_row_data(inscode, 1)
        if data2_3:
            result.append(data2_3.pMeDem)  # 2
            result.append(data2_3.pMeOf)  # 3
        else:
            result.append(data2_3)  # 2
            result.append(data2_3)  # 3

        # columns 4 to 14
        data4_14 = closing_price_info_service.get_list_data(inscode)
        result = result + data4_14

        # column 15 to 21
        data15_21 = instrument_info_Service.get_list_data(inscode)
        result = result + data15_21

        # column 22
        data22 = closing_price_info_service.get_closing_price_info_by_inscode(inscode)
        result.append(None)

        # column 23,24
        data23_24 = instrument_info_Service.get_instrument_info_by_id(inscode)
        if data23_24:
            result.append(data23_24.sectorPE)  # 23
            result.append(data23_24.psr)  # 24
        else:
            result.append(None)
            result.append(None)

        # column 25 to 32
        data25_32 = client_type_service.get_list_data(inscode)
        if data25_32:
            result = result + data25_32
        else:
            result.append(None)

        # column 33 to 52
        data33_52 = best_limits_service.get_list_data(inscode)
        if data33_52:
            result = result + data33_52
        else:
            result.append(None)

        # column 53
        data53 = closing_price_info_service.get_closing_price_info_by_inscode(inscode)
        if data53:
            result.append(data53.hEven)
        else:
            result.append(None)

        if result[19] and result[5]:
            if float(result[19]) != 0:
                value22 = str(round(float(result[5]) / float(result[19]), 2))
                result[20] = value22

        if result[5] and result[15]:
            value12 = str(float(result[15]) * float(result[5]))
            result[10] = value12

        return result
