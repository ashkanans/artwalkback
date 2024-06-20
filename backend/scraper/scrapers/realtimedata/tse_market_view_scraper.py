from datetime import datetime

import jdatetime as jdatetime

from backend.scraper.realtimedata.service.tse_market_view_service import TseMarketViewService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.market_overview_service import MarketOverviewService
from backend.scraper.tsetmc.service.selected_indexes_service import SelectedIndexesService


class TseMarketViewScraper(BaseScraper):
    def process_data(self, data):

        tse_market_view_service = TseMarketViewService()
        tse_market_view_service.create_table()
        tse_market_view_service.delete_all_tse_market_view_entries()  # We have to remove this line in furture, but it's work for now
        rows = []

        rowdata = self.fill_row()
        today_date = jdatetime.date.today()
        rowdata.insert(0, str(today_date))
        rows.append(rowdata)

        if rows:
            for row in rows:
                tse_market_view_service.update_tse_market_view_entry(row)

    def fill_row(self):

        # make instances
        selected_indexes_service = SelectedIndexesService()
        market_overview = MarketOverviewService()

        result = []
        # columns 2 to 4
        data2_4 = selected_indexes_service.get_selected_indexes_by_name('شاخص كل')
        if data2_4:
            result.append(self.rounding(data2_4.xDrNivJIdx004, 2))  # 2
            result.append(self.rounding(data2_4.indexChange, 2))  # 3
            value = str(
                round((float(data2_4.indexChange) / (float(data2_4.xDrNivJIdx004) - float(data2_4.indexChange)) * 100),
                      2))
            result.append(value)  # 4
        else:
            result.append(data2_4)  # 2
            result.append(data2_4)  # 3
            result.append(data2_4)  # 4

        # columns 5 to 7
        data5_7 = selected_indexes_service.get_selected_indexes_by_name('شاخص كل (هم وزن)')
        if data5_7:
            result.append(self.rounding(data5_7.xDrNivJIdx004, 2))  # 5
            result.append(self.rounding(data5_7.indexChange, 2))  # 6
            value = str(round(
                (float(data5_7.indexChange) / (float(data5_7.xDrNivJIdx004) - float(data5_7.indexChange)) * 100),
                2))
            result.append(value)  # 7
        else:
            result.append(data5_7)  # 5
            result.append(data5_7)  # 6
            result.append(data5_7)  # 7

        # columns 8 to 12
        data8_12 = market_overview.get_market_overview_by_id("بازار نقدی بورس")
        result.append(self.rounding(data8_12.marketValue, 2))  # 8
        date_object = datetime.strptime(str(data8_12.marketActivityDEven), "%Y%m%d")
        solar_date = jdatetime.date.fromgregorian(day=date_object.day, month=date_object.month, year=date_object.year)
        result.append(
            str(solar_date) + " " + str(datetime.strptime(str(data8_12.marketActivityHEven), "%H%M%S").time()))  # 9
        result.append(self.rounding(data8_12.marketActivityZTotTran, 2))  # 10
        result.append(self.rounding(data8_12.marketActivityQTotCap, 2))  # 11
        result.append(self.rounding(data8_12.marketActivityQTotTran, 2))  # 12

        # column 13 to 15
        data13_15 = selected_indexes_service.get_selected_indexes_by_name('شاخص كل فرابورس')
        if data13_15:
            result.append(self.rounding(data13_15.xDrNivJIdx004, 2))  # 13
            result.append(self.rounding(data13_15.indexChange, 2))  # 14
            value = str(
                round((float(data13_15.indexChange) / (
                        float(data13_15.xDrNivJIdx004) - float(data13_15.indexChange)) * 100),
                      2))
            result.append(value)  # 15
        else:
            result.append(data13_15)  # 13
            result.append(data13_15)  # 14
            result.append(data13_15)  # 15

        # column 16 to 18
        data16_18 = selected_indexes_service.get_selected_indexes_by_name('شاخص كل هم وزن فرابورس')
        if data16_18:
            result.append(self.rounding(data16_18.xDrNivJIdx004, 2))  # 16
            result.append(self.rounding(data16_18.indexChange, 2))  # 17
            value = str(
                round((float(data16_18.indexChange) / (
                        float(data16_18.xDrNivJIdx004) - float(data16_18.indexChange)) * 100),
                      2))
            result.append(value)  # 18
        else:
            result.append(data16_18)  # 16
            result.append(data16_18)  # 17
            result.append(data16_18)  # 18

        # columns 19 to 24
        data19_24 = market_overview.get_market_overview_by_id("فرا بورس")
        result.append(self.rounding(data19_24.marketValue, 2))  # 19
        result.append(self.rounding(data19_24.marketValueBase, 2))  # 20
        date_object = datetime.strptime(str(data19_24.marketActivityDEven), "%Y%m%d")
        solar_date = jdatetime.date.fromgregorian(day=date_object.day, month=date_object.month,
                                                  year=date_object.year)
        result.append(
            str(solar_date) + " " + str(datetime.strptime(str(data19_24.marketActivityHEven), "%H%M%S").time()))  # 21
        result.append(self.rounding(data19_24.marketActivityZTotTran, 2))  # 22
        result.append(self.rounding(data19_24.marketActivityQTotCap, 2))  # 23
        result.append(self.rounding(data19_24.marketActivityQTotTran, 2))  # 24

        return result

    def rounding(self, value, digitNumber):
        return str(round(float(value), digitNumber))
