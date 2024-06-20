from backend.export.excel.dummy_workbook import DummyWorkbook
from backend.scraper.realtimedata.service.sector_stock_price_service import SectorStockPriceService
from backend.scraper.scrapers.base_scraper import BaseScraper


class SectorStockPriceScraper(BaseScraper):
    def process_data(self, data):
        sector = self.config.get('sectors')
        for sector_code, indexes in sector.items():
            dummyWorkbook = DummyWorkbook()
            dummyWorkbook.fill_dummy_sheet_with_sector_prices_with_cells(sector_code, indexes)
            rows = dummyWorkbook.get_rows_from_workbook()

            sectorStockPriceService = SectorStockPriceService(f"sector_stock_price_{int(sector_code)}")
            sectorStockPriceService.create_table()
            sectorStockPriceService.delete_all_sector_stock_price_entries()

            i = 0
            for row in rows:
                row = (i,) + row
                sectorStockPriceService.update_sector_stock_price(row)
                i += 1
