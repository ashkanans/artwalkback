import os
from unittest import TestCase

from werkzeug.datastructures import FileStorage

from backend.utils.web.utils import go_up_levels
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.user import UserService
from web_app import app


class TestServicesFileToText(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user_service = UserService()
        self.username = 'example'
        self.password = 'example'
        self.email = 'example.com'

        self.user = self.user_service.create_user(username=self.username, password=self.password, email=self.email)

        self.token = Authenticator().generate_auth_token(user_id=self.user.user_id, username=self.username)

    def tearDown(self):
        self.user_service.delete_user_by_username(self.username)

    def test_file_to_text(self):
        current_working_directory = os.getcwd()
        new_directory = go_up_levels(current_working_directory, 2)
        example_file_abs_path = os.path.join(new_directory, 'files',
                                             'example.pdf')  # Use os.path.join to ensure correct path construction

        # Create a FileStorage object for the file
        with open(example_file_abs_path, 'rb') as file:
            file_storage = FileStorage(file)
            file_storage.filename = 'example.pdf'  # Set filename

            # Send request with valid authentication token and file
            response = self.client.post('/api/services/file_to_text',
                                        data={'files': {'file': file_storage}},
                                        headers={'Authorization': "Bearer " + self.token},
                                        content_type='multipart/form-data',
                                        buffered=True,
                                        )

        # self.assertEqual(response.status_code, 200)
