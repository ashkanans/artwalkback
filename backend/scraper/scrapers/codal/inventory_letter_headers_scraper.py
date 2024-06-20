from backend.export.excel.dummy_workbook import DummyWorkbook
from backend.scraper.codal.service.cells_service import CellsService
from backend.scraper.codal.service.inventory_letter_headers_service import InventoryLetterHeadersService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService


class InventoryLetterHeadersScraper(BaseScraper):
    def process_data(self, data):
        instrumentInfoService = InstrumentInfoService()
        persian_symbols = instrumentInfoService.get_all_persian_symbols_by_sector_code(13)

        cellsService = CellsService()

        for symbol in persian_symbols:

            letters = cellsService.get_cells_id_symbol_for_inventory_letter(symbol.replace("ك", "ک"))
            if letters[0]:
                dummyWorkbook = DummyWorkbook()
                dummyWorkbook.get_invertory_table_headers(letters[0], letters[1])
                rows = dummyWorkbook.get_rows_from_workbook()

                InventoryLetterHeadersservice = InventoryLetterHeadersService()
                InventoryLetterHeadersservice.create_table()

                row_dict = {}
                for row in rows:
                    if row[0]:
                        row = row + (symbol,)
                        row = (row[0] +' ' + row[2],) + row[1:]
                        row_dict['id'] = row[0]
                        row_dict['type'] = row[1]
                        row_dict['symbol'] = row[2]
                        InventoryLetterHeadersservice.update_entry(row_dict)

