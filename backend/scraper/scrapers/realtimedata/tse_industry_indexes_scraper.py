from backend.scraper.realtimedata.service.tse_industry_indexes_service import TseIndustryIndexesService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.all_indexes_service import AllIndexesService

headers = [' نام صنعت ', 'مقدار', 'تغییر', 'درصد']


class TseIndustryIndexesScraper(BaseScraper):
    def process_data(self, data):

        tse_industry_indexes_service = TseIndustryIndexesService()
        tse_industry_indexes_service.create_table()
        tse_industry_indexes_service.delete_all_tse_industry_indexes_entries()

        desired_indexes = ['01', '10', '13', '14', '17', '19', '20', '21', '22', '23', '25', '27', '28', '29', '31',
                           '32', '34', '38', '39', '40', '42', '43', '44', '47', '49', '53',
                           '54', '56', '57', '58', '60', '64', '65', '67', '70', '72', '73', '74',
                           'استخراج نفت جزكشف11', 'بيمه و بازنشسته66', 'شاخص 30 شركت بزرگ']

        rows = [headers]
        for index in desired_indexes:
            rowdata = self.fill_row(index)
            rows.append(rowdata)

        if rows:
            for row in rows:
                tse_industry_indexes_service.update_tse_industry_indexes_entry(row)

    def fill_row(self, index):
        result = []
        tse_all_indexes = AllIndexesService()

        data = tse_all_indexes.get_data_contain_specifi_value_in_name(index)

        result.append(data.lVal30)
        result.append(self.rounding(data.xDrNivJIdx004, 2))
        result.append(self.rounding(data.indexChange, 2))
        value = str(round(
            (float(data.indexChange) / (float(data.xDrNivJIdx004) - float(data.indexChange)) * 100),
            2))
        result.append(value)

        return result

    def rounding(self, value, digitNumber):
        return str(round(float(value), digitNumber))
