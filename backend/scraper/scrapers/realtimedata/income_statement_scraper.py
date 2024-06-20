from backend.export.excel.dummy_workbook import DummyWorkbook
from backend.scraper.codal.service.cells_service import CellsService
from backend.scraper.realtimedata.service.income_statement_service import IncomeStatementService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService


class IncomeStatementScraper(BaseScraper):
    def process_data(self, data):
        instrumentInfoService = InstrumentInfoService()
        persian_symbols = instrumentInfoService.get_all_persian_symbols_by_sector_code(13)

        cellsService = CellsService()

        for symbol in persian_symbols:
            insId = instrumentInfoService.get_instrument_info_by_persian_symbol(
                symbol.replace('ی', 'ي').replace("ک", "ك")).insCode
            letters = cellsService.get_cells_id_symbol_for_income_statement(symbol.replace("ك", "ک"))
            if letters:
                dummyWorkbook = DummyWorkbook()
                dummyWorkbook.fill_dummy_sheet_with_income_statement_with_cells(letters, symbol)
                rows = dummyWorkbook.get_rows_from_workbook()

                # rows.pop(len(rows)-1)
                IncomeStatementservice = IncomeStatementService(f"income_statement_{insId}")
                IncomeStatementservice.create_table()
                IncomeStatementservice.delete_all_income_statement_entries()

                i = 0
                for row in rows:
                    row = (i,) + row
                    if row[1] != '1000':
                        IncomeStatementservice.update_income_statement_entry(row)
                    i += 1
