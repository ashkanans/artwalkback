import hashlib
import os
from datetime import datetime
from io import BytesIO

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.ocr.ocr_converted_files import OCRConvertedFile

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)

API_URL = 'https://www.eboo.ir/api/ocr/getway'
EBOO_TOKE = 'ffpKNwZNYYydB7FcI0MpI6h0xdwZpZfu'


class OCRService:
    def __init__(self):
        pass

    def create_ocr_file(self, id, type, name, hash, converted_word, source, converted_txt):
        session = Session()
        new_file = OCRConvertedFile(id=id, type=type, name=name, hash=hash, converted_word=converted_word,
                                    converted_txt=converted_txt,
                                    source=source, insert_date_time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        session.add(new_file)
        session.commit()
        session.close()

    def get_ocr_file(self, id):
        session = Session()
        file = session.query(OCRConvertedFile).filter_by(id=id).first()
        session.close()
        return file

    def get_ocr_file_by_hash_type_name(self, hash, type, name):
        session = Session()
        file = session.query(OCRConvertedFile).filter_by(hash=hash, name=name, type=type).first()
        session.close()
        return file

    def update_ocr_file(self, id, new_name=None, new_hash=None, new_converted_word=None):
        session = Session()
        file = session.query(OCRConvertedFile).filter_by(id=id).first()
        if file:
            if new_name:
                file.name = new_name
            if new_hash:
                file.hash = new_hash
            if new_converted_word:
                file.converted_word = new_converted_word
            session.commit()
        session.close()

    def delete_ocr_file(self, id):
        session = Session()
        file = session.query(OCRConvertedFile).filter_by(id=id).first()
        if file:
            session.delete(file)
            session.commit()
        session.close()

    def get_all_ocr_files(self):
        session = Session()
        files = session.query(OCRConvertedFile).all()
        session.close()
        return files

    def save_uploaded_file(self, ocr_file, upload_folder):
        """
        Save the uploaded file to the specified upload folder.
        """
        ocr_filename, ocr_extension = os.path.splitext(ocr_file.filename)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_ocr_filename = f"file_{current_datetime}{ocr_extension}"
        ocr_file.save(os.path.join(upload_folder, new_ocr_filename))
        return ocr_filename, new_ocr_filename, ocr_extension

    def get_download_link(self, upload_folder, new_ocr_filename):
        """
        Construct the download link for the uploaded file.
        """
        download_link = f"http://46.100.50.100:63932/{upload_folder}/{new_ocr_filename}"
        return download_link

    def get_file_hash(self, file_path):
        """
        Calculate the hash of the file content.
        """
        with open(file_path, 'rb') as file:
            file_content = file.read()
            file_hash = hashlib.sha512(file_content).hexdigest()
        return file_hash

    def send_to_ocr_service(self, download_link):
        """
        Send the file to the OCR service for processing.
        """
        payload = {
            'token': EBOO_TOKE,
            'command': 'addfile',
            'filelink': download_link
        }
        response = requests.post(API_URL, json=payload, timeout=30)
        return response

    def convert_file(self, file_token, method):
        """
        Convert the file using the OCR service.
        """
        convert_payload = {
            'token': EBOO_TOKE,
            'command': 'convert',
            'filetoken': file_token,
            'method': method
        }
        convert_response = requests.post(API_URL, json=convert_payload)
        return convert_response

    def download_word_file(self, word_url):
        """
        Download the Word file from the OCR service.
        """
        word_response = requests.get(word_url)
        return word_response

    def save_word_file(self, word_response, word_folder, new_ocr_filename):
        """
        Save the Word file to the specified folder.
        """
        word_filename = f"{new_ocr_filename[:-4]}.docx"
        with open(os.path.join(word_folder, word_filename), 'wb') as word_file:
            word_file.write(word_response.content)
        return word_filename

    def handle_existing_file(self, ocr_file, word_folder):
        """
        Handle the case where the OCR file already exists.
        """
        ocr_content = ocr_file.converted_word
        if ocr_content:
            word_filename = f"{ocr_file.name}.docx"
            word_content = BytesIO(ocr_content)
            with open(os.path.join(word_folder, word_filename), 'wb') as word_file:
                word_file.write(word_content.getvalue())
            return word_filename
        else:
            return None
