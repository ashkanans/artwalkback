import unicodedata


class KeywordCounter:
    @staticmethod
    def normalize_text(text):
        # Replace Arabic characters with Persian equivalents
        text = unicodedata.normalize('NFKC', text).replace('ك', 'ک').replace('ي', 'ی')
        # Normalize text to NFKC form to ensure consistent encoding
        return text

    @staticmethod
    def count_occurrences(text, keywords):
        # Combine Persian and Arabic characters in the regex pattern
        persian_arabic_pattern = r'[^آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیء-ي]'

        # Clean the text by replacing non-Persian and non-Arabic characters with a space
        cleaned_text = re.sub(persian_arabic_pattern, ' ', text)
        cleaned_text = cleaned_text.replace("\n", " ")

        # Normalize the cleaned text
        cleaned_text = KeywordCounter.normalize_text(cleaned_text)

        keyword_occurrences = {}

        for keyword in keywords:
            keyword = keyword.strip()
            # Normalize the keyword
            keyword = KeywordCounter.normalize_text(keyword)
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            occurrences = len(pattern.findall(cleaned_text))
            keyword_occurrences[keyword] = occurrences

        return keyword_occurrences


import os
import re
import uuid

from docx import Document

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.ocr.service import OCRService
from web_app import app


class ServicesCountOccurrencesHandler:
    def __init__(self, authenticator: Authenticator):
        self.ocr_service = OCRService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            ocr_file = request.files['file']
            keywords = request.form['keywords']

            # Check if the file is a PDF
            if ocr_file.filename == '':
                return MESSAGES['NO_FILE_SELECTED']['NO_FILE_SELECTED']

            if not keywords:
                return MESSAGES['OCR_PROCESSING']['NO_KEYWORDS_PROVIDED']

            keywords = keywords.split(',')

            # Check if the file is a PDF
            if ocr_file.filename == '':
                return MESSAGES['OCR_PROCESSING']['FILENAME_EMPTY']

            supported_extensions = ('.pdf', '.jpg', '.jpeg', '.png', '.bmp')
            if ocr_file and ocr_file.filename.lower().endswith(supported_extensions):
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])

                original_filename, new_ocr_filename, ocr_extension = self.ocr_service.save_uploaded_file(
                    ocr_file, app.config['UPLOAD_FOLDER'])
                download_link = self.ocr_service.get_download_link(app.config['UPLOAD_FOLDER'], new_ocr_filename)
                original_file_hash = self.ocr_service.get_file_hash(
                    os.path.join(app.config['UPLOAD_FOLDER'], new_ocr_filename))

                ocr_file = self.ocr_service.get_ocr_file_by_hash_type_name(
                    hash=original_file_hash, type=ocr_extension[1:], name=original_filename)

                if True:
                    response = self.ocr_service.send_to_ocr_service(download_link)
                    response_data = response.json()

                    if response_data.get('Status'):
                        if response_data.get('Status') == 'Done':
                            highest_keyword_occurrences = {}

                            convert_methods = [int(method) for method in response_data['ConvertMethods'].split(',')]
                            for method in convert_methods:
                                convert_response = self.ocr_service.convert_file(response_data.get('FileToken'),
                                                                                 method=method)

                                if convert_response.status_code == 200:
                                    convert_response_data = convert_response.json()

                                    if convert_response_data.get('Status') == 'Done':
                                        word_url = convert_response_data.get('FileToDownload')
                                        word_response = self.ocr_service.download_word_file(word_url)

                                        if word_response.status_code == 200:
                                            if not os.path.exists(app.config['WORD_FOLDER']):
                                                os.makedirs(app.config['WORD_FOLDER'])

                                            word_filename = self.ocr_service.save_word_file(
                                                word_response, app.config['WORD_FOLDER'], new_ocr_filename)

                                            self.ocr_service.create_ocr_file(
                                                id=uuid.uuid4().hex,
                                                type=ocr_extension[1:],
                                                name=original_filename,
                                                hash=original_file_hash,
                                                converted_word=word_response.content,
                                                source="WEB_APP"
                                            )
                                            file_path = os.path.join(app.config['WORD_FOLDER'], word_filename)
                                            text = self.read_docx(file_path)

                                            # Count occurrences of keywords for this method
                                            keyword_occurrences = KeywordCounter.count_occurrences(text, keywords)

                                            # Update highest count for each keyword
                                            for keyword, count in keyword_occurrences.items():
                                                if keyword not in highest_keyword_occurrences or count > \
                                                        highest_keyword_occurrences[keyword]:
                                                    highest_keyword_occurrences[keyword] = count

                                        else:
                                            return MESSAGES['OCR_PROCESSING']['FAILED_TO_DOWNLOAD_WORD']
                                    else:
                                        return MESSAGES['OCR_PROCESSING']['CONVERT_PDF_FAILED']
                                else:
                                    return MESSAGES['FILE_UPLOAD']['FAILED_TO_CONVERT_PDF'](convert_response)

                            self.response = highest_keyword_occurrences
                            return self.response
                        else:
                            return MESSAGES['FILE_UPLOAD']['FAILED_TO_ADD_PDF'](response_data)
                    else:
                        return MESSAGES['FILE_UPLOAD']['FAILED_TO_SEND_TO_API'](response)
                else:
                    word_filename = self.ocr_service.handle_existing_file(ocr_file, app.config['WORD_FOLDER'])
                    if word_filename:
                        file_path = os.path.join(app.config['WORD_FOLDER'], word_filename)
                        text = self.read_docx(file_path)

                        highest_keyword_occurrences = {}

                        for method in range(1, 5):
                            # Assuming the text remains the same for the file, otherwise call OCR service again.
                            keyword_occurrences = KeywordCounter.count_occurrences(text, keywords)

                            # Update highest count for each keyword
                            for keyword, count in keyword_occurrences.items():
                                if keyword not in highest_keyword_occurrences or count > highest_keyword_occurrences[
                                    keyword]:
                                    highest_keyword_occurrences[keyword] = count

                        self.response = highest_keyword_occurrences
                        return self.response
                    else:
                        return MESSAGES['OCR_PROCESSING']['EMPTY_OCR']
            else:
                return MESSAGES['FILE_UPLOAD']['NOT_SUPPORTED_FILE']
        else:
            return self.authenticator.message

    def read_docx(self, file_path):
        doc = Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
