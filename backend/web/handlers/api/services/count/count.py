import os
import re
import uuid

from backend.utils.services.tesseract import ocr
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.ocr.service import OCRService
from web_app import app


class ServicesCountHandler:
    def __init__(self, authenticator: Authenticator):
        self.ocr_service = OCRService()
        self.authenticator = authenticator
        self.response = {"": ""}
        self.refined_text: str = ""

    @staticmethod
    def count_occurrences(text, keywords):
        # Combine Persian and Arabic characters in the regex pattern
        persian_arabic_pattern = r'[^آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیء-ي]'

        # Clean the text by replacing non-Persian and non-Arabic characters with a space
        cleaned_text = re.sub(persian_arabic_pattern, ' ', text)
        cleaned_text = cleaned_text.replace("\n", " ")

        keyword_occurrences = {}

        for keyword in keywords:
            keyword = keyword.strip()
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            occurrences = len(pattern.findall(cleaned_text))
            keyword_occurrences[keyword] = occurrences

        return keyword_occurrences

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
                original_file_hash = self.ocr_service.get_file_hash(
                    os.path.join(app.config['UPLOAD_FOLDER'], new_ocr_filename))

                ocr_saved_file = self.ocr_service.get_ocr_file_by_hash_type_name(
                    hash=original_file_hash, type=ocr_extension[1:], name=original_filename)

                # check if file exist in database
                if ocr_saved_file is not None:
                    read_text = ocr_saved_file.converted_txt.decode('utf-8')
                    keyword_occurrences = self.count_occurrences(read_text, keywords)
                    return keyword_occurrences

                self.refined_text, text = ocr.ocr_pdf(os.path.join(app.config['UPLOAD_FOLDER'], new_ocr_filename))
                try:
                    text_file = open("temp.txt", "w+", encoding="utf-8")
                    text_file.write(self.refined_text)
                    text_file.close()
                    with open('temp.txt', 'rb') as file:
                        converted_txt_content = file.read()

                    self.ocr_service.create_ocr_file(
                        id=uuid.uuid4().hex,
                        type=ocr_extension[1:],
                        name=original_filename,
                        hash=original_file_hash,
                        converted_txt=converted_txt_content,
                        converted_word=None,
                        source="WEB_APP"
                    )

                except Exception as e:
                    print("exception", e)
                    raise e
                finally:
                    os.remove("temp.txt")

                keyword_occurrences = self.count_occurrences(self.refined_text, keywords)
                return keyword_occurrences

            else:
                return MESSAGES['FILE_UPLOAD']['NOT_SUPPORTED_FILE']
        else:
            return self.authenticator.message
