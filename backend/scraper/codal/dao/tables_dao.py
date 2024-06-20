from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound

from backend.scraper.codal.model.tables import Tables
from backend.scraper.logger.base_logger import BaseLogger


class TablesDAO(BaseLogger):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def create_table(self):
        """
        Create the 'tables' table if it does not exist.
        """
        if not self.table_exists():
            try:
                self.logger.info(f"Creating table: {Tables.__tablename__}")
                Tables.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info(f"Table: {Tables.__tablename__} created.")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table: {Tables.__tablename__} already exists.")
        return False

    def table_exists(self):
        """
        Check if the 'tables' table exists in the database.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(Tables.__tablename__)

    def save_table(self, data):
        """
        Save a new table record in the 'tables' table.
        """
        table = Tables(**data)
        self.session.add(table)
        self.session.commit()
        self.logger.info(f"Table saved, tablesId: f{table.tablesId}")
        return table.tablesId

    def get_all_tables(self):
        """
        Retrieve all table records from the 'tables' table.
        """
        return self.session.query(Tables).all()

    def get_table_by_id(self, tables_id):
        """
        Retrieve a table record from the 'tables' table by its ID.
        """
        try:
            return self.session.query(Tables).filter_by(tablesId=tables_id).first()
        except NoResultFound:
            return None
    def get_table_by_titleFa(self,title_fa):
        """
        Retrieve a table record from the 'tables' table by its title_Fa.
        """
        try:
            return self.session.query(Tables).filter_by(title_Fa=title_fa).first()
        except NoResultFound:
            return None

    def delete_table(self, tables_id):
        """
        Delete a table record from the 'tables' table by its ID.
        """
        table = self.session.query(Tables).filter_by(tablesId=tables_id).first()
        if table:
            self.session.delete(table)
            self.session.commit()
            return True
        return False

    def update_table(self, data):
        """
        Update a table record in the 'tables' table by its ID.
        If the record does not exist, create a new one.
        """
        tableId = data.get('tablesId')
        existing_record = self.get_table_by_id(tableId)
        if existing_record:
            # Update the existing record with new values
            for key, value in data.items():
                setattr(existing_record, key, value)

            # Commit the changes
            self.session.commit()
            self.logger.info(f"Table updated, tablesId: f{existing_record.tablesId}")
            return existing_record.tablesId

        else:
            # If no record found, insert a new one
            return self.save_table(data)
