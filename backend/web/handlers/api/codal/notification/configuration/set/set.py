import multiprocessing
from datetime import datetime

from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.codal.service import CodalService
from backend.web.service.user import UserService


class CodalNotificationConfigurationSetHandler:
    def __init__(self, authenticator: Authenticator):
        self.codalService = CodalService()
        self.userService = UserService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:

            data = request.json

            step1_data = data.get('step1', {})
            step2_data = data.get('step2', [])
            step3_data = data.get('step3', [])
            step4_data = data.get('step4', {})

            including = step1_data.get('including', '')
            excluding = step1_data.get('excluding', '')

            publisher_national_code = ','.join(step2_data)

            letter_types = ','.join(step3_data)

            period = step4_data.get('period')
            letters_checked = step4_data.get('lettersChecked', False)
            attachments_checked = step4_data.get('attachmentsChecked', False)

            user_id = self.authenticator.user_id
            username = self.authenticator.username

            existing_configs = self.codalService.get_notitification_configutaion_by_user_id_list(user_id)

            including_items = [item.strip() for item in including.split("،")]
            excluding_items = [item.strip() for item in excluding.split("،")]
            national_code_items = [item.strip() for item in publisher_national_code.split(",")]
            letter_type_items = [item.strip() for item in letter_types.split(",")]

            if not existing_configs:

                self.response = MESSAGES['NOTIFICATION']['CONFIGURATION_SET_SUCCESSFUL']
            else:

                self.codalService.delete_all_notification_configuration_by_user_id(user_id)

                self.codalService.delete_all_notifications_by_user_id(user_id)

                self.response = MESSAGES['NOTIFICATION']['CONFIGURATION_MODIFIED_SUCCESSFUL']

            for including_item in including_items:
                for excluding_item in excluding_items:
                    for national_code_item in national_code_items:
                        for letter_type_item in letter_type_items:
                            self.codalService.add_notification_configuration(
                                user_id=user_id,
                                including=including_item,
                                excluding=excluding_item,
                                publisher_national_code=national_code_item,
                                letter_types=letter_type_item,
                                period=period,
                                lettersChecked=letters_checked,
                                attachmentsChecked=attachments_checked
                            )

            process = multiprocessing.Process(target=self.execute_async_task, args=(user_id,))
            process.start()

            user = self.userService.get_user_by_username(username)
            self.userService.update_user(user.user_id, user.username, user.email, user.password_hash, True,
                                         datetime.now())

            return self.response
        else:
            return self.authenticator.message

    def execute_async_task(self, user_id):
        self.codalService.process_notitification_configutaion_by_username(user_id)
