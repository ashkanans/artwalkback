from sqlalchemy import inspect, asc
from sqlalchemy.exc import NoResultFound

from backend.scraper.codal.model.sheets import Sheets
from backend.scraper.logger.base_logger import BaseLogger


class SheetsDAO(BaseLogger):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def create_table(self):
        """
        Create the 'sheets' table if it does not exist.
        """
        if not self.table_exists():
            try:
                self.logger.info(f"Creating table: {Sheets.__tablename__}")
                Sheets.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info(f"Table: {Sheets.__tablename__} created.")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table: {Sheets.__tablename__} already exists.")
        return False

    def table_exists(self):
        """
        Check if the 'sheets' table exists in the database.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(Sheets.__tablename__)

    def save_sheet(self, data):
        """
        Save a new sheet record in the 'sheets' table.
        """
        sheet = Sheets(**data)
        self.session.add(sheet)
        self.session.commit()
        self.logger.info(f"Sheet saved, sheetsId: f{sheet.sheetsId}")
        return sheet.sheetsId

    def get_all_sheets(self):
        """
        Retrieve all sheet records from the 'sheets' table.
        """
        return self.session.query(Sheets).all()

    def get_sheet_by_id(self, sheets_id):
        """
        Retrieve a sheet record from the 'sheets' table by its ID.
        """
        try:
            return self.session.query(Sheets).filter_by(sheetsId=sheets_id).one()
        except NoResultFound:
            return None

    def get_all_sheet_by_id(self, sheets_id):
        """
        Retrieve a sheet record from the 'sheets' table by its ID.
        """
        try:
            return self.session.query(Sheets).filter_by(sheetsId=sheets_id).order_by(asc(Sheets.tablesId)).all()
        except NoResultFound:
            return None

    def get_all_sheet_by_title(self, title_fa,id):
        """
        Retrieve a sheet record from the 'sheets' table by its ID.
        """
        try:
            return self.session.query(Sheets).filter_by(sheetsId=id).filter(Sheets.title_Fa.like(f"%{title_fa}%")).order_by(
                asc(Sheets.tablesId)).all()
        except NoResultFound:
            return None

    def delete_sheet(self, sheets_id):
        """
        Delete a sheet record from the 'sheets' table by its ID.
        """
        sheet = self.session.query(Sheets).filter_by(sheetsId=sheets_id).first()
        if sheet:
            self.session.delete(sheet)
            self.session.commit()
            return True
        return False

    def update_sheet(self, data):
        """
        Update a sheet record in the 'sheets' table by its ID.
        If the record does not exist, create a new one.
        """

        tables_id = data['tablesId']
        existing_record = self.get_sheet_by_tables_id(tables_id)

        if existing_record:
            # Update the existing record with new values
            for key, value in data.items():
                setattr(existing_record, key, value)

            # Commit the changes
            self.session.commit()
            self.logger.info(f"Sheet updated, tablesId: f{existing_record.tablesId}")
            return existing_record.tablesId

        else:
            # If no record found, insert a new one
            return self.save_sheet(data)

    def get_sheet_by_tables_id(self, tables_id):
        """
        Retrieve a sheet record from the 'sheets' table by its ID.
        """
        try:
            return self.session.query(Sheets).filter_by(tablesId=tables_id).one()
        except NoResultFound:
            return None
