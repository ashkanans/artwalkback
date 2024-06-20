from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.get_related_company import GetRelatedCompany

Base = declarative_base()


class GetRelatedCompanyDao(BaseLogger):

    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the GetRelatedCompanyDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_get_related_company(self, data):
        """
               Saves a new get related company entry.

               Parameters:
               - data (dict): Dictionary containing closing price daily list data.

               Returns:
               - datetime: Saved closing price daily list entry's datetime
               """
        get_related_company = GetRelatedCompany(**data)
        self.session.add(get_related_company)
        self.session.commit()
        self.logger.info(f"get related companys entry saved: {get_related_company.insCode}")
        return get_related_company.insCode

    def get_get_related_company_by_inscode(self, inscode):
        """
        Retrieves a get related companys entry by its inscode.

        Parameters:
        - code (str): get related companys entry inscode to retrieve.

        Returns:
        - main groups or None: Retrieved get related companys entry or None if not found.
        """
        return self.session.query(GetRelatedCompany).filter_by(insCode=inscode).first()

    def get_all_get_related_company_entries(self):
        """
        Retrieves all get related companys  entries.

        Returns:
        - list: List of all get related companys  entries.
        """
        return self.session.query(GetRelatedCompany).all()

    def update_get_related_company(self, data):
        """
        Updates a get related companys entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated get related companys entry's inscode
        """
        updated_ids = []

        try:
            existing_record = self.get_get_related_company_by_inscode(data.get("insCode"))
            if existing_record:
                for inscode, value in data.items():
                    setattr(existing_record, inscode, value)

                self.session.commit()
                self.logger.info(f"Updated get related companys entry with inscode: {existing_record.insCode}")
                updated_ids.append(existing_record.insCode)
            else:
                self.save_get_related_company(data)

        except NoResultFound:
            updated_ids.append(self.save_get_related_company(data))

        return updated_ids

    def delete_get_related_company_by_inscode(self, inscode):
        """
        Deletes a get related companys entry by its inscode.

        Parameters:
        - code (str): get related companys entry inscode to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        get_related_company = self.session.query(GetRelatedCompany).filter_by(inscode=inscode).first()
        if get_related_company:
            self.session.delete(get_related_company)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the get_related_company table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(GetRelatedCompany.__tablename__)

    def create_table(self):
        """
        Create the tse_get_related_company table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                GetRelatedCompany.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
