def custom_message(message_type, message_content):
    return {message_type: message_content}


MESSAGES = {
    'AUTHENTICATION': {
        'AUTHORIZED': {'message': 'Authorized'},
        'NOT_AUTHORIZED': {'error': 'Not authorized'},
        'TOKEN_NOT_FOUND': {'error': 'Token was not found in the header'},
        'REGISTRATION_SUCCESSFUL': {'success': True, 'message': 'User registered successfully'},
        'CUSTOM_MESSAGE': custom_message
    },
    'FILE_UPLOAD': {
        'NO_FILE_SELECTED': {'error': 'No file selected'},
        'NOT_SUPPORTED_FILE': {
            'error': 'Not supported file, Please upload a file having types: .pdf, .jpg, .jpeg, .png, .bmp'},
        'FAILED_TO_CONVERT_PDF': lambda convert_response: {
            'error': f'Failed to convert PDF file: Error {convert_response.status_code}'},
        'FAILED_TO_ADD_PDF': lambda response_data: {
            'error': f'Failed to add PDF file: Error {response_data.get("Status")}'},
        'FAILED_TO_SEND_TO_API': lambda response: {
            'error': f'Failed to send PDF file to eboo.ir API: Error {response.status_code}'},
        'CUSTOM_MESSAGE': custom_message
    },
    'OCR_PROCESSING': {
        'EMPTY_OCR': {'error': 'OCR content is empty'},
        'FAILED_TO_DOWNLOAD_WORD': {'error': 'Failed to download Word file'},
        'CONVERT_PDF_FAILED': {'error': 'Failed to convert PDF file'},
        'CUSTOM_MESSAGE': custom_message
    },
    'DATA_PROCESSING': {
        'NO_KEYWORDS_PROVIDED': {'error': 'No keywords provided'},
        'FILENAME_EMPTY': {'error': 'filename is empty!'},
        'CUSTOM_MESSAGE': custom_message
    },
    'REGISTRATION': {
        'ERROR_REGISTERING_USER': lambda e: {'success': False, 'message': f'Error registering user: {str(e)}'},
        'USER_ALREADY_EXISTS': lambda username: {'success': False, 'message': f'User already exists: {username}'}
    },
    'LOGIN': {
        'AUTHENTICATION_SUCCESSFUL': lambda token, username, user_info: {'message': 'Authentication successful',
                                                                    'token': token,
                                                                         'user': user_info},
        'ERROR_CHECKING_CREDENTIALS': lambda e: {'message': f'Error checking login credentials: {str(e)}'}
    },
    'SETTING': {
        'SUCCESSFUL_SET': {'message': 'Setting set successful'}
    },
    'NOTIFICATION': {
        'CONFIGURATION_SET_SUCCESSFUL': {'message': 'Notification configuration set successful'},
        'CONFIGURATION_MODIFIED_SUCCESSFUL': {'message': 'Notification configuration modified successful'}
    }
}
