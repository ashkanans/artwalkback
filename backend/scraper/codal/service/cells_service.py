import time
from collections import defaultdict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.codal.dao.cells_dao import CellsDAO
from backend.scraper.codal.service.letters_map_service import LettersMapService
from backend.scraper.codal.service.sheets_service import SheetsService
from backend.scraper.codal.service.tables_service import TablesService

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


def persian_to_gregorian(persian_date_str):
    # Define a dictionary mapping Persian month names to their lengths in days
    persian_months = {
        1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31,
        7: 30, 8: 30, 9: 30, 10: 30, 11: 30, 12: 29 if (int(persian_date_str[:4]) % 4 == 0) else 30
    }

    # Split the Persian date string into year, month, and day components
    persian_year, persian_month, persian_day = map(int, persian_date_str.split()[0].split('/'))

    # Calculate the number of days since the epoch (Farvardin 1, 1)
    days_since_epoch = (persian_year - 1) * 365 + ((persian_year - 1) // 33 * 8) + \
                       sum(persian_months[i] for i in range(1, persian_month)) + persian_day

    # Calculate the number of leap days
    leap_days = ((persian_year - 1) // 33 + 1) * 8

    # Add the leap days to the total
    days_since_epoch += leap_days

    # Adjust the days for the 1979 leap year (optional)
    if persian_year > 1357:
        days_since_epoch += 11

    # Convert the number of days since the epoch to a Gregorian date
    gregorian_year = 621 + days_since_epoch // 365
    remainder_days = days_since_epoch % 365
    gregorian_month = 1
    gregorian_day = 0

    while remainder_days > 0:
        gregorian_month_days = 31 if gregorian_month in [1, 3, 5, 7, 8, 10, 12] else \
            30 if gregorian_month in [4, 6, 9,
                                      11] else 29 if gregorian_year % 4 == 0 and gregorian_year % 100 != 0 or gregorian_year % 400 == 0 else 28

        if remainder_days >= gregorian_month_days:
            remainder_days -= gregorian_month_days
            gregorian_month += 1
        else:
            gregorian_day = remainder_days + 1
            break

    # Format the Gregorian date as a string
    gregorian_date_str = f"{gregorian_year:04d}/{gregorian_month:02d}/{gregorian_day:02d} {persian_date_str.split()[1]}"

    return gregorian_date_str


def filter_duplicates(thisYearsLetters):
    thisYearsLetters.sort(key=lambda x: (x.periodEndToDate, x.kind != "1"))

    selected_letters = defaultdict(list)

    for letter in thisYearsLetters:
        selected_letters[letter.reportName].append(letter)

    # Filter out the duplicates, choosing the one with kind == "1"
    filtered_letters = [letters[0] for letters in selected_letters.values()]
    filtered_letters.sort(key=lambda x: persian_to_gregorian(x.registerDateTime), reverse=True)
    return filtered_letters


class CellsService:
    def __init__(self):
        """
        Initializes the CellsService.

        Parameters:
        - session: SQLAlchemy session object
        """

        self.cells_dao = CellsDAO(session)

    def save_cell(self, data):
        """
        Saves a new cell.

        Parameters:
        - data (dict): Dictionary containing cell data.

        Returns:
        - Cells: Saved cell object.
        """
        return self.cells_dao.save_cell(data)

    def get_all_cells(self):
        """
        Retrieves all cells.

        Returns:
        - list: List of all cells.
        """
        return self.cells_dao.get_all_cells()

    def get_cell_by_id(self, cells_id):
        """
        Retrieves a cell by its ID.

        Parameters:
        - cells_id (int): ID of the cell to retrieve.

        Returns:
        - Cells or None: Retrieved cell or None if not found.
        """
        return self.cells_dao.get_cell_by_id(cells_id)

    def update_cell(self, cellDict: dict):
        """
        Updates a cell.

        Parameters:
        - cells_id (int): ID of the cell to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - Cells or None: Updated cell object or None if not found.
        """
        cellIdList = list(cellDict.keys())
        cellsListOrg = list(cellDict.values())
        for i in range(len(cellsListOrg)):
            cellsList = cellsListOrg[i]
            for cell in cellsList:
                cell["cellId"] = cellIdList[i]
                cell = {key: str(value) for key, value in cell.items()}
                self.cells_dao.update_cell(cell)

    def delete_cell(self, cells_id):
        """
        Deletes a cell by its ID.

        Parameters:
        - cells_id (int): ID of the cell to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.cells_dao.delete_cell(cells_id)

    def create_table(self):
        """
        Create the cells table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.cells_dao.create_table()

    def get_cells_by_id_and_symbol(self, cell_symbol):
        """
        Retrieves a cell by its ID.

        Parameters:
        - cells_id (int): ID of the cell to retrieve.

        Returns:
        - Cells or None: Retrieved cell or None if not found.
        """
        lettersMapService = LettersMapService()
        sheetsService = SheetsService()
        tablesService = TablesService()

        # Get the current time before executing the statements
        start_time = time.time()

        # Execute the statements
        thisYearsLetters = lettersMapService.get_recent_letters_by_symbol(cell_symbol)
        # Calculate the time taken for the first statement
        first_statement_time = time.time() - start_time

        # Reset the start time
        start_time = time.time()

        thisYearsLetters = filter_duplicates(thisYearsLetters)

        # Calculate the time taken for the second statement
        second_statement_time = time.time() - start_time

        start_time = time.time()

        thisYearsLettersSheets = sheetsService.get_sheets_by_list_of_letters_maps(thisYearsLetters)

        # Calculate the time taken for the third statement
        third_statement_time = time.time() - start_time

        start_time = time.time()

        thisYearsLettersSheetsTables = tablesService.get_sheets_by_list_of_sheetIds(thisYearsLettersSheets)

        # Calculate the time taken for the fourth statement
        fourth_statement_time = time.time() - start_time

        start_time = time.time()

        thisYearsLettersSheetsTablesCells = self.get_cells_by_list_of_tableIds(thisYearsLettersSheetsTables)

        # Calculate the time taken for the fifth statement
        fifth_statement_time = time.time() - start_time

        # Print the time taken for each statement
        # print("Time taken for the first statement:", first_statement_time)
        # print("Time taken for the second statement:", second_statement_time)
        # print("Time taken for the third statement:", third_statement_time)
        # print("Time taken for the fourth statement:", fourth_statement_time)
        # print("Time taken for the fifth statement:", fifth_statement_time)

        return thisYearsLettersSheetsTablesCells

    def get_cells_id_symbol_for_income_statement(self, cell_symbol):
        """
        Retrieves a cell by its ID.

        Parameters:
        - cells_id (int): ID of the cell to retrieve.

        Returns:
        - Cells or None: Retrieved cell or None if not found.
        """
        lettersMapService = LettersMapService()
        sheetsService = SheetsService()
        tablesService = TablesService()

        # Get the current time before executing the statements
        start_time = time.time()

        # Execute the statements
        thisYearsLetters = lettersMapService.get_income_statemenet_letters(cell_symbol, 'صورت‌های مالی')
        # Calculate the time taken for the first statement
        first_statement_time = time.time() - start_time

        # Reset the start time
        start_time = time.time()

        thisYearsLetters = filter_duplicates(thisYearsLetters)

        # Calculate the time taken for the second statement
        second_statement_time = time.time() - start_time

        start_time = time.time()

        thisYearsLettersSheets = sheetsService.get_sheets_by_title_and_list_of_letters_maps(thisYearsLetters,'سود و زیان')

        # Calculate the time taken for the third statement
        third_statement_time = time.time() - start_time

        start_time = time.time()

        thisYearsLettersSheetsTables = tablesService.get_sheets_by_list_of_sheetIds(thisYearsLettersSheets,'سود و زیان')

        # Calculate the time taken for the fourth statement
        fourth_statement_time = time.time() - start_time

        start_time = time.time()

        thisYearsLettersSheetsTablesCells = self.get_cells_by_list_of_tableIds(thisYearsLettersSheetsTables)

        # Calculate the time taken for the fifth statement
        fifth_statement_time = time.time() - start_time

        # Print the time taken for each statement
        # print("Time taken for the first statement:", first_statement_time)
        # print("Time taken for the second statement:", second_statement_time)
        # print("Time taken for the third statement:", third_statement_time)
        # print("Time taken for the fourth statement:", fourth_statement_time)
        # print("Time taken for the fifth statement:", fifth_statement_time)

        return thisYearsLettersSheetsTablesCells

    def get_cells_id_symbol_for_inventory_letter(self, cell_symbol):
        """
        Retrieves a cell by its ID.

        Parameters:
        - cells_id (int): ID of the cell to retrieve.

        Returns:
        - Cells or None: Retrieved cell or None if not found.
        """
        lettersMapService = LettersMapService()
        sheetsService = SheetsService()
        tablesService = TablesService()

        # Get the current time before executing the statements
        start_time = time.time()

        # Execute the statements
        thisYearsLetters = lettersMapService.get_income_statemenet_letters(cell_symbol, 'صورت‌های مالی')

        thisYearsLetters = filter_duplicates(thisYearsLetters)

        thisYearsLettersSheets = sheetsService.get_sheets_by_title_and_list_of_letters_maps(thisYearsLetters,
                                                                                            'گزارش تفسیری')

        thisYearsLettersSheetsTables = tablesService.get_sheets_by_list_of_table_title(thisYearsLettersSheets)

        thisYearsLettersSheetsTablesCells = self.get_cells_by_list_of_tableIds(thisYearsLettersSheetsTables[0])

        return [thisYearsLettersSheetsTablesCells, thisYearsLettersSheetsTables[1]]

    def get_cells_by_list_of_tableIds(self, letters):

        letters_with_cells = {}
        for key, tables in letters.items():
            cells = []
            for table in tables:
                cells.append(self.get_cell_by_id(table.cellsId))
                letters_with_cells[key] = cells
        return letters_with_cells

    def get_final_mpr_cells(self, symbol):
        lettersMapService = LettersMapService()
        sheetsService = SheetsService()
        tablesService = TablesService()

        thisYearsLetters = lettersMapService.get_recent_letters_by_symbol(symbol)
        if len(thisYearsLetters):
            finalMprLetter = [thisYearsLetters[0]]
            finalMprLetterSheets = sheetsService.get_sheets_by_list_of_letters_maps(finalMprLetter)
            finalMprLetterSheetsTables = tablesService.get_sheets_by_list_of_sheetIds(finalMprLetterSheets)
            finalMprLetterSheetsTablesCells = self.get_cells_by_list_of_tableIds(finalMprLetterSheetsTables)
            return finalMprLetterSheetsTablesCells

        return None
