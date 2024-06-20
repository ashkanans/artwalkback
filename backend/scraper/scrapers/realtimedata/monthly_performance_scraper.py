from backend.export.excel.dummy_workbook import DummyWorkbook
from backend.scraper.codal.service.cells_service import CellsService
from backend.scraper.realtimedata.service.monthly_performance_service import MonthlyPerformanceService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService
from backend.utils.scraper.realtimedata.utils import convert_arabic_to_persian


class MonthlyPerformanceScraper(BaseScraper):
    def process_data(self, data):
        instrumentInfoService = InstrumentInfoService()
        persian_symbols = instrumentInfoService.get_all_persian_symbols_by_sector_code(13)
        persian_symbols = ["شرانل", "شبهرن", "شنفت", "شسپا", "فسازان"]
        cellsService = CellsService()

        for symbol in persian_symbols:
            insId = instrumentInfoService.get_instrument_info_by_persian_symbol(
                symbol.replace('ی', 'ي').replace("ک", "ك")).insCode
            letters = cellsService.get_cells_by_id_and_symbol(symbol.replace("ك", "ک"))
            if letters:
                dummyWorkbook = DummyWorkbook()
                dummyWorkbook.fill_dummy_sheet_with_monthly_performance_with_cells(letters,
                                                                                   convert_arabic_to_persian(symbol))
                rows = dummyWorkbook.get_rows_from_workbook()

                monthlyPerformanceService = MonthlyPerformanceService(f"monthly_performance_{insId}")
                monthlyPerformanceService.create_table()
                monthlyPerformanceService.delete_all_final_mpr_entries()

                i = 0
                for row in rows:
                    row = (i,) + row
                    monthlyPerformanceService.update_monthly_performance_entry(row)
                    i += 1
