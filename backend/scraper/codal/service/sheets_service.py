from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.codal.dao.sheets_dao import SheetsDAO

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class SheetsService:
    def __init__(self):
        """
        Initializes the SheetsService.

        Parameters:
        - session: SQLAlchemy session object
        """

        self.sheets_dao = SheetsDAO(session)

    def save_sheet(self, data):
        """
        Saves a new sheet.

        Parameters:
        - data (dict): Dictionary containing sheet data.

        Returns:
        - Sheets: Saved sheet object.
        """
        return self.sheets_dao.save_sheet(data)

    def get_all_sheets(self):
        """
        Retrieves all sheets.

        Returns:
        - list: List of all sheets.
        """
        return self.sheets_dao.get_all_sheets()

    def get_sheet_by_id(self, sheets_id):
        """
        Retrieves a sheet by its ID.

        Parameters:
        - sheets_id (int): ID of the sheet to retrieve.

        Returns:
        - Sheets or None: Retrieved sheet or None if not found.
        """
        return self.sheets_dao.get_sheet_by_id(sheets_id)

    def get_all_sheet_by_id(self, sheets_id):
        """
        Retrieves a sheet by its ID.

        Parameters:
        - sheets_id (int): ID of the sheet to retrieve.

        Returns:
        - Sheets or None: Retrieved sheet or None if not found.
        """
        return self.sheets_dao.get_all_sheet_by_id(sheets_id)

    def get_all_sheet_by_title(self, title_fa,id):

        return self.sheets_dao.get_all_sheet_by_title(title_fa,id)


    def update_sheet(self, sheet, tableIdList):
        """
        Updates a sheet.

        Parameters:
        - sheets_id (int): ID of the sheet to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - Sheets or None: Updated sheet object or None if not found.
        """
        for tableId in tableIdList:
            sheet["tablesId"] = tableId
            sheet = {key: str(value) for key, value in sheet.items()}
            self.sheets_dao.update_sheet(sheet)

    def delete_sheet(self, sheets_id):
        """
        Deletes a sheet by its ID.

        Parameters:
        - sheets_id (int): ID of the sheet to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.sheets_dao.delete_sheet(sheets_id)

    def create_table(self):
        """
        Create the sheets table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.sheets_dao.create_table()

    def get_sheets_by_list_of_letters_maps(self, letters):
        letters_with_sheetNo = {}
        for letter in letters:
            letters_with_sheetNo[letter.tracingNo] = self.get_all_sheet_by_id(letter.sheetsId)
        return letters_with_sheetNo

    def get_sheets_by_title_and_list_of_letters_maps(self, letters,title):
        letters_with_sheetNo = {}
        for letter in letters:
            data = self.get_all_sheet_by_title(title,letter.sheetsId)
            if data:
                letters_with_sheetNo[letter.tracingNo] = data
        return letters_with_sheetNo
