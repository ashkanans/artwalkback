import json
import random
import re

from bs4 import BeautifulSoup

from backend.scraper.codal.service.cells_service import CellsService
from backend.scraper.codal.service.letters_map_service import LettersMapService
from backend.scraper.codal.service.sheets_service import SheetsService
from backend.scraper.codal.service.tables_service import TablesService
from backend.scraper.scrapers.base_scraper import BaseScraper


class LetterCellsScraper(BaseScraper):

    def process_data(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')

        company = soup.find('span', {'id': 'ctl00_txbCompanyName'})
        if company:
            company = company.text.strip()

        listed_capital = soup.find('span', {'id': 'ctl00_lblListedCapital'})
        if listed_capital:
            listed_capital = listed_capital.text.strip()

        symbol = soup.find('span', {'id': 'ctl00_lblDisplaySymbol'})
        if symbol:
            if not len(str(symbol)) == 0:
                symbol = symbol.text.strip()
                symbol = re.sub(r'[^\w\s]', '', symbol)
        if not symbol:
            symbol = soup.find('span', {'id': 'ctl00_txbSymbol'})
            if symbol:
                symbol = symbol.text.strip()

        unauthorized_capital = soup.find('span', {'id': 'ctl00_txbUnauthorizedCapital'})
        if unauthorized_capital:
            unauthorized_capital = unauthorized_capital.text.strip()

        priode = soup.find('span', {'id': 'ctl00_lblPeriodEndToDate'})
        report_name = soup.find('span', {'id': 'ctl00_lblReportName'})
        if priode:
            priode = priode.text.strip()
            report_name = report_name.text.strip()
            # report_name = f"گزارش فعالیت ماهانه  1 ماهه منتهی به {priode}"
            report_name = f" منتهی به {report_name} {priode}"

        company_state = soup.find('span', {'id': 'ctl00_lblCompanyState'})
        if company_state:
            company_state = company_state.text.strip()

        isic = soup.find('span', {'id': 'ctl00_lblISIC'})
        if isic:
            isic = isic.text.strip()

        script_tags = soup.find_all('script')
        for script in script_tags:
            javascript_code = script.text if script else ''
            match = re.search(r'var datasource = (\{.*?\});', javascript_code)

            if match:
                print("'datasource' variable found in the JavaScript code.")
                json_data = match.group(1)
                data_dict = json.loads(json_data)

                first_seed = data_dict.get("tracingNo")
                random.seed(first_seed)
                sheets_id = random.randrange(10 ** 9, 10 ** 10)
                sheet_components_id = 1

                print(f"Number of sheets in: {len(data_dict.get('sheets'))}")
                sheets = data_dict.get('sheets')[0]
                print(f"Number of tables in: {len(sheets.get('tables'))}")
                tables = sheets.get('tables')

                tables_with_ids = {random.randrange(10 ** 9, 10 ** 10): table for table in tables}
                cells_with_ids = {random.randrange(10 ** 9, 10 ** 10): table.pop('cells') for table in
                                  tables_with_ids.values()}

                data_dict.pop('sheets')
                sheets.pop('tables')
                if 'sheetComponents' in sheets:
                    sheets.pop('sheetComponents')

                data_dict.update({
                    "sheetsId": sheets_id,
                    "company": company,
                    "listedCapital": listed_capital,
                    "symbol": symbol,
                    "unauthorizedCapital": unauthorized_capital,
                    "reportName": report_name,
                    "companyState": company_state,
                    "isic": isic
                })

                sheets.update({
                    "sheetsId": sheets_id,
                    "sheetComponentsId": sheet_components_id
                })

                letters_map_service = LettersMapService()
                sheets_service = SheetsService()
                table_service = TablesService()
                cells_service = CellsService()

                letters_map_service.create_table()
                sheets_service.create_table()
                table_service.create_table()
                cells_service.create_table()

                try:
                    cells_service.update_cell(cells_with_ids)
                    table_service.update_table(tables_with_ids, cells_with_ids)
                    sheets_service.update_sheet(sheets, list(tables_with_ids.keys()))
                    letters_map_service.update_letters_map(data_dict)
                except Exception as e:
                    print(f"Error updating tables for url:{self.url}", e)
                    return
