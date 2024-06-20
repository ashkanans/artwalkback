import datetime
import errno
import os

import pandas as pd
from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.model.app.chart_data import data_list_to_dict
from backend.web.service.app.service import AppService


class AppChartdataexcelHandler:
    def __init__(self, authenticator: Authenticator):
        self.appService = AppService()
        self.authenticator = authenticator
        self.response_base_url = "http://46.100.50.100:63938/excel_files/"
        self.response = None

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            data = request.get_json()
            parameters = data['parameters']
            date_range = data['date_range']
            setting = data['setting']

            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            excel_filename = f"chart_data_{timestamp}.xlsx"
            excel_directory = "excel_files"
            excel_path = os.path.join(excel_directory, excel_filename)

            self.ensure_directory(excel_directory)

            writer = pd.ExcelWriter(excel_path, engine='openpyxl')

            for id in parameters:
                chart_data = self.appService.get_chart_data(id=id, from_date=date_range['from'],
                                                            to_date=date_range['to'], date_type="gr")

                data_dict = data_list_to_dict(chart_data)

                df = pd.DataFrame(data_dict)

                data_list_id = self.appService.get_chartId_by_id(id=id)
                df.to_excel(writer, sheet_name=f"{data_list_id.level4}", index=False)

            writer.close()

            self.response = f"{self.response_base_url}{excel_filename}"

            return self.response
        else:
            return self.authenticator.message

    def ensure_directory(self, directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
