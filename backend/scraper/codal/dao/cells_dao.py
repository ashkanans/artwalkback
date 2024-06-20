from sqlalchemy import inspect, asc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.codal.model.cells import Cells
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class CellsDAO(BaseLogger):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def create_table(self):
        """
        Create the 'cells' table if it does not exist.
        """
        if not self.table_exists():
            try:
                self.logger.info(f"Creating table: {Cells.__tablename__}")
                Cells.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info(f"Table: {Cells.__tablename__} created.")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {Cells.__tablename__}  already exists.")
        return False

    def table_exists(self):
        """
        Check if the 'cells' table exists in the database.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(Cells.__tablename__)

    def save_cell(self, cell):
        """
        Save a new cell record in the 'cells' table.
        """
        cell = Cells(**cell)
        self.session.add(cell)
        self.session.commit()
        self.logger.info(f"Cell saved, cellId: f{cell.cellId}, address: {cell.address}")
        return cell.cellId

    def get_all_cells(self):
        """
        Retrieve all cell records from the 'cells' table.
        """
        return self.session.query(Cells).all()

    def get_cell_by_id(self, cells_id):
        """
        Retrieve a cell record from the 'cells' table by its ID.
        """
        try:
            return self.session.query(Cells).filter_by(cellId=cells_id).order_by(asc(Cells.address)).all()
        except NoResultFound:
            return None

    def delete_cell(self, cells_id):
        """
        Delete a cell record from the 'cells' table by its ID.
        """
        cell = self.session.query(Cells).filter_by(cellsId=cells_id).first()
        if cell:
            self.session.delete(cell)
            self.session.commit()
            return True
        return False

    def update_cell(self, cell):
        """
        Update a cell record in the 'cells' table by its ID.
        If the record does not exist, create a new one.
        """

        # Attempt to retrieve the existing record based on cells_id
        existing_record = self.get_cell_by_id_and_address(cell)

        if existing_record:
            # Update the existing record with new values
            for key, value in cell.items():
                setattr(existing_record, key, value)

            # Commit the changes
            self.session.commit()
            self.logger.info(f"Cell updated, cellId: f{existing_record.cellId}, address: {existing_record.address}")
            return existing_record.cellId

        else:
            # If no record found, insert a new one
            return self.save_cell(cell)

    def get_cell_by_id_and_address(self, cell):
        return self.session.query(Cells).filter_by(address=cell.get('address'),
                                                   cellId=cell.get('cellId')).first()
