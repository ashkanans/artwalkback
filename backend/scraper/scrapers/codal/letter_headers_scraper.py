from backend.scraper.codal.service.cells_service import CellsService
from backend.scraper.codal.service.letter_headers_service import LettersRowHeadersService, \
    LettersColumnHeadersMapService
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.instrument_info_service import InstrumentInfoService
from backend.utils.export.excel.utils import excel_cell_to_row_col
from backend.utils.scraper.realtimedata.utils import convert_persian_to_arabic


# Define a custom sorting key function
def address_sort_key(cell):
    # Split the address string into its components (e.g., "A1" -> ["A", "1"])
    address_parts = cell.address.split("A")
    # Convert the numeric part of the address to an integer for sorting
    numeric_part = int(address_parts[1])
    return numeric_part


def get_headers(cells):
    domestic_headers = []
    export_headers = []
    service_income_headers = []
    sales_return_headers = []

    cells_with_A = [cell for cell in cells if "A" in cell.address]

    # Sort the filtered list based on the address field
    cells_with_A = sorted(cells_with_A, key=address_sort_key)

    cell_domestic_sales = None
    cell_export_sales = None
    cell_service_income = None
    cell_sales_return = None

    for cell in cells_with_A:
        if 'فروش داخلی' in cell.value and 'جمع' not in cell.value:
            cell_domestic_sales = cell
        elif 'فروش صادراتی' in cell.value and 'جمع' not in cell.value:
            cell_export_sales = cell
        elif 'درآمد ارائه خدمات' in cell.value and 'جمع' not in cell.value:
            cell_service_income = cell
        elif 'برگشت از فروش' in cell.value and 'جمع' not in cell.value:
            cell_sales_return = cell

    if cell_domestic_sales:
        domestic_sales_col, domestic_sales_row = excel_cell_to_row_col(cell_domestic_sales.address)
    if cell_export_sales:
        export_sales_col, export_sales_row = excel_cell_to_row_col(cell_export_sales.address)
    if cell_service_income:
        service_income_col, service_income_row = excel_cell_to_row_col(cell_service_income.address)
    if cell_sales_return:
        sales_return_col, sales_return_row = excel_cell_to_row_col(cell_sales_return.address)

    for cell in cells_with_A:
        col, row = excel_cell_to_row_col(cell.address)
        if domestic_sales_row < row < export_sales_row:
            if not cell.value == "":
                domestic_headers.append(cell.value)

        elif export_sales_row < row < service_income_row:
            if not cell.value == "":
                export_headers.append(cell.value)

        elif service_income_row < row < sales_return_row:
            if not cell.value == "":
                service_income_headers.append(cell.value)

        elif sales_return_row < row:
            if not cell.value == "" and not cell.value == "جمع":
                sales_return_headers.append(cell.value)

            elif cell.value == "جمع":
                break

    results = {}
    results['فروش داخلی'] = domestic_headers
    results['فروش صادراتی'] = export_headers
    results['درآمد ارائه خدمات'] = service_income_headers
    results['برگشت از فروش'] = sales_return_headers

    return results


class LetterHeadersScraper(BaseScraper):

    def process_data(self, data):
        instrumentService = InstrumentInfoService()
        cellsService = CellsService()
        lettersRowHeadersService = LettersRowHeadersService()
        lettersColumnHeadersMapService = LettersColumnHeadersMapService()

        if not lettersRowHeadersService.table_exists():
            lettersRowHeadersService.create_table()

        values = instrumentService.get_all_persian_symbols()
        for id in values:
            insCode = instrumentService.get_instrument_info_by_persian_symbol(convert_persian_to_arabic(id)).insCode
            finalLetters = cellsService.get_cells_by_id_and_symbol(id.replace('ی', 'ي'))
            if finalLetters:
                finalLetter = next(iter(finalLetters.items()))
                first_list_of_cells = finalLetter[1][0]
                headers = get_headers(first_list_of_cells)
                lettersRowHeadersService.update_entry(headers, id.strip(), int(insCode))

            else:
                print(f"Final letter not found for {id}")
