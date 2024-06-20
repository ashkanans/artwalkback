from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.codal.model.letter_headers import LettersColumnHeadersMap, LettersRowHeaders
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class LettersColumnHeadersMapDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def save_entry(self, data):
        entry = LettersColumnHeadersMap(**data)
        self.session.add(entry)
        self.session.commit()
        self.logger.info(f"Saved entry with ID: {entry.id}")
        return entry

    def get_all_entries(self):
        return self.session.query(LettersColumnHeadersMap).all()

    def get_entry_by_id(self, entry_id):
        return self.session.query(LettersColumnHeadersMap).filter_by(id=entry_id).first()

    def update_entry(self, data):
        existing_entry = self.session.query(LettersColumnHeadersMap).filter_by(id=data.get("id")).first()
        if existing_entry:
            for key, value in data.items():
                setattr(existing_entry, key, value)
            self.session.commit()
            self.logger.info(f"Updated entry with ID: {existing_entry.id}")
            return existing_entry
        else:
            return self.save_entry(data)

    def delete_entry_by_id(self, entry_id):
        entry = self.session.query(LettersColumnHeadersMap).filter_by(id=entry_id).first()
        if entry:
            self.session.delete(entry)
            self.session.commit()
            self.logger.info(f"Deleted entry with ID: {entry_id}")
            return True
        return False

    def table_exists(self):
        inspector = inspect(self.session.bind)
        return inspector.has_table(LettersColumnHeadersMap.__tablename__)

    def create_table(self):
        if not self.table_exists():
            try:
                LettersColumnHeadersMap.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created successfully.")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()
                return False
        else:
            self.logger.info("Table already exists.")
            return False


class LettersRowHeadersDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def save_entry(self, data):
        entry = LettersRowHeaders(**data)
        self.session.add(entry)
        self.session.commit()
        self.logger.info(f"Saved entry with ID: {entry.id}")
        return entry

    def get_all_entries(self):
        return self.session.query(LettersRowHeaders).all()

    def get_entry_by_id(self, entry_id):
        return self.session.query(LettersRowHeaders).filter_by(id=entry_id).first()

    def update_entry(self, data):
        existing_entry = self.session.query(LettersRowHeaders).filter_by(insCode=data.get("insCode"),
                                                                         header_key=data.get("header_key"),
                                                                         header_item=data.get("header_item")).first()
        if existing_entry:
            for key, value in data.items():
                setattr(existing_entry, key, value)
            self.session.commit()
            self.logger.info(f"Updated entry with ID: {existing_entry.id}")
            return existing_entry
        else:
            return self.save_entry(data)

    def delete_entry_by_id(self, entry_id):
        entry = self.session.query(LettersRowHeaders).filter_by(id=entry_id).first()
        if entry:
            self.session.delete(entry)
            self.session.commit()
            self.logger.info(f"Deleted entry with ID: {entry_id}")
            return True
        return False

    def table_exists(self):
        inspector = inspect(self.session.bind)
        return inspector.has_table(LettersRowHeaders.__tablename__)

    def create_table(self):
        if not self.table_exists():
            try:
                LettersRowHeaders.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created successfully.")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()
                return False
        else:
            self.logger.info("Table already exists.")
            return False

    def get_entry_by_symbol(self, symbol):
        return reversed(self.session.query(LettersRowHeaders).filter_by(symbol=symbol).all())
