from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.codal.dao.tables_dao import TablesDAO

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class TablesService:
    def __init__(self):
        """
        Initializes the TablesService.

        Parameters:
        - session: SQLAlchemy session object
        """
        # Creating the SQLAlchemy engine
        self.tables_dao = TablesDAO(session)

    def save_table(self, data):
        """
        Saves a new table.

        Parameters:
        - data (dict): Dictionary containing table data.

        Returns:
        - Tables: Saved table object.
        """
        return self.tables_dao.save_table(data)

    def get_all_tables(self):
        """
        Retrieves all tables.

        Returns:
        - list: List of all tables.
        """
        return self.tables_dao.get_all_tables()

    def get_table_by_id(self, tables_id):
        """
        Retrieves a table by its ID.

        Parameters:
        - tables_id (int): ID of the table to retrieve.

        Returns:
        - Tables or None: Retrieved table or None if not found.
        """
        return self.tables_dao.get_table_by_id(tables_id)

    def get_table_by_titleFa(self, title_fa):
        return self.tables_dao.get_table_by_titleFa(title_fa)

    def update_table(self, tables, cells):
        """
        Updates a table.

        Parameters:
        - tables_id (int): ID of the table to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - Tables or None: Updated table object or None if not found.
        """
        cellIdList = list(cells.keys())

        tablesIdList = list(tables.keys())
        tablesListOrg = list(tables.values())

        for i in range(len(tablesListOrg)):
            table = tablesListOrg[i]
            table["tablesId"] = tablesIdList[i]
            table["cellsId"] = cellIdList[i]
            table = {key: str(value) for key, value in table.items()}
            self.tables_dao.update_table(table)

    def delete_table(self, tables_id):
        """
        Deletes a table by its ID.

        Parameters:
        - tables_id (int): ID of the table to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.tables_dao.delete_table(tables_id)

    def create_table(self):
        """
        Create the tables table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.tables_dao.create_table()

    def get_sheets_by_list_of_sheetIds(self, letters,title):
        letters_with_tracingNo_and_tableNo = {}
        for key, tables in letters.items():
            table_id_by_sheetNo = []
            for table in tables:
                table = self.get_table_by_id(table.tablesId)
                if title in table.title_Fa:

                    table_id_by_sheetNo.append(table)

            table_id_by_sheetNo.sort(key=lambda x: x.code)
            letters_with_tracingNo_and_tableNo[key] = table_id_by_sheetNo
        return letters_with_tracingNo_and_tableNo

    def get_sheets_by_list_of_table_title(self, letters):
        letters_with_tracingNo_and_tableNo = {}
        table_titles = []
        for key, tables in letters.items():
            table_id_by_sheetNo = []

            for table in tables:
                table = self.get_table_by_id(table.tablesId)
                if table.title_Fa == 'گردش مقداری - ریالی موجودی کالا' or table.title_Fa == 'خرید و مصرف مواد اولیه':
                    table_id_by_sheetNo.append((table, table.title_Fa))

            # Sort both the tables and titles based on the table's code
            table_id_by_sheetNo.sort(key=lambda x: x[0].code)
            letters_with_tracingNo_and_tableNo[key] = [table for table, title in table_id_by_sheetNo]
            table_titles = [title for table, title in table_id_by_sheetNo]

        return [letters_with_tracingNo_and_tableNo, table_titles]
