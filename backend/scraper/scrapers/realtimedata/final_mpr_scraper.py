from backend.export.excel.dummy_workbook import DummyWorkbook
from backend.scraper.codal.service.cells_service import CellsService
from backend.scraper.realtimedata.service.final_mpr_service import FinalMprService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService


class FinalMprScraper(BaseScraper):
    def process_data(self, data):

        instrumentInfoService = InstrumentInfoService()
        persian_symbols = self.config.get("instruments")
        cellsService = CellsService()

        for symbol in persian_symbols:
            insId = instrumentInfoService.get_instrument_info_by_persian_symbol(
                symbol.replace("ک", "ك").replace("ی", "ي")).insCode
            letters = cellsService.get_cells_by_id_and_symbol(symbol.replace("ك", "ک").replace("ی", "ي"))
            if letters:
                final_letter_tracingNo, final_letter_cell_list = next(iter(letters.items()))
                dummyWorkbook = DummyWorkbook()
                dummyWorkbook.fill_dummy_sheet_with_final_mpr_with_cells(final_letter_cell_list)
                rows = dummyWorkbook.get_rows_from_workbook()

                final_mpr_service = FinalMprService(f"final_mpr_{insId}")
                final_mpr_service.create_table()
                final_mpr_service.delete_all_final_mpr_entries()

                i = 0
                for row in rows:
                    row = (i,) + row
                    final_mpr_service.update_final_mpr_entry(row)
                    i += 1
            else:
                self.logger.warning(f"No letters found for symbol: {symbol}, insCode: {insId}")

