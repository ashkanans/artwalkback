from backend.export.excel.dummy_workbook import DummyWorkbook
from backend.scraper.codal.service.cells_service import CellsService
from backend.scraper.realtimedata.service.inventory_letter_service import InventoryLetterService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService
from backend.utils.scraper.realtimedata.utils import convert_arabic_to_persian


class InventoryLetterScraper(BaseScraper):
    def process_data(self, data):
        instrumentInfoService = InstrumentInfoService()
        persian_symbols = instrumentInfoService.get_all_persian_symbols_by_sector_code(1)
        persian_symbols = ['پکرمان']
        cellsService = CellsService()

        for symbol in persian_symbols:
            insId = instrumentInfoService.get_instrument_info_by_persian_symbol(
                symbol.replace('ی', 'ي').replace("ک", "ك")).insCode
            letters = cellsService.get_cells_id_symbol_for_inventory_letter(symbol.replace("ك", "ک"))
            if letters:
                dummyWorkbook = DummyWorkbook()
                dummyWorkbook.fill_dummy_sheet_with_inventory_letter_with_cells(letters[0],
                                                                                   convert_arabic_to_persian(symbol))
                rows = dummyWorkbook.get_rows_from_workbook()

                InventoryLetterservice = InventoryLetterService(f"inventory_letter_{insId}")
                InventoryLetterservice.create_table()
                InventoryLetterservice.delete_all_inventory_letter_entries()

                i = 0
                for row in rows:
                    row = (i,) + row
                    InventoryLetterservice.update_inventory_letter_entry(row)
                    i += 1
