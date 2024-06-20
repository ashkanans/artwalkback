import json
import logging
import os
import socket
import time
from abc import ABC
from multiprocessing import Pool, cpu_count

import jsonpickle
import requests

from backend.engine.socket_log import SocketLog
from backend.engine.update.TaskStatus import TaskStatus
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.scrapers.request_method import RequestMethod
from backend.scraper.scrapers.response_types import ResponseType


class BaseScraper(ABC, BaseLogger):
    def __init__(self, ip='localhost', port=9090):
        super().__init__()
        self.response = None
        self.config = None
        self.data = {}
        self.url = None
        self.logger = logging.getLogger(__name__)
        self.url_index = None
        self.max_processes = cpu_count()  # Get the number of available CPU cores

        self.ip = ip
        self.port = port
        self.progress_socket = socket.socket()
        self.socket_log = SocketLog("", TaskStatus.PENDING, 0, -1)

    def create_socket_connection(self):
        try:
            self.progress_socket = socket.socket()
            self.progress_socket.connect((self.ip, self.port))
        except Exception as e:
            print(f"Error creating connection: {e}")

    def send_progress(self, status: TaskStatus, progress: int, total: int):

        self.socket_log.name = self.config['name']
        self.socket_log.status = status
        self.socket_log.progress = progress
        self.socket_log.total = total
        self.create_socket_connection()
        try:
            json_string = jsonpickle.encode(self.socket_log)
            self.progress_socket.send(json_string.encode())
            message = self.progress_socket.recv(1024)
            message = message.decode()
            self.progress_socket.close()
        except Exception as e:
            print(f"Error creating table: {e}")
    def add_config(self, config):
        self.config = config

    def fetch_data_from_urls(self):

        if self.config['ResponseType'] == ResponseType.NONE.value:
            self.process_data(data=[])
        elif self.config['ResponseType'] == ResponseType.SELENDIOUM.value:
            self.process_data(self.config['urls'])
        else:
            with Pool(processes=min(1, self.max_processes)) as pool:
                pool.map(self.fetch_data, enumerate(self.config['urls']))

    def fetch_data(self, url_index_url):

        url_index, url = url_index_url
        self.url_index = url_index
        self.url = url
        success = self.make_request(url, url_index)
        if success and self.response.status_code == 200:
            try:
                if self.config['ResponseType'] == ResponseType.JSON.value:
                    json_data = self.response.json()
                    self.data = {url: json_data}
                    # self.send_progress(TaskStatus.PROCESS_DATA, 0, len(self.config['urls']))
                    self.process_data(json_data)
                    # self.send_progress(TaskStatus.COMPLETED, 0, len(self.config['urls']))
                elif self.config['ResponseType'] == ResponseType.HTML.value:
                    self.process_data(self.response)
            except json.JSONDecodeError as e:
                self.logger.error(f"Error processing response for index: {self.url_index}, {url}: {e}")
                return
        else:
            self.logger.warning(f"Failed to fetch data from {url}. Status code: {self.response.status_code}")

    def make_request(self, url, url_index):
        success = False
        max_retries = 3
        retry_delay = 1  # in seconds

        for _ in range(max_retries):
            try:
                request_method = RequestMethod(self.config.get('requestMethod', RequestMethod.GET.value))
                if request_method == RequestMethod.POST:
                    if self.config['type'] == 'fipiran':
                        self.response = requests.post(url, headers=self.config['header'],
                                                      data=self.config.get('postParams')[url_index])
                    else:
                        self.response = requests.post(url, headers=self.config['header'],
                                                      data=json.dumps(self.config.get('postParams')))
                else:
                    self.response = requests.get(url, headers=self.config['header'])

                # Check if the request was successful
                self.response.raise_for_status()
                # If successful, set the success flag and break out of the loop
                success = True
                self.logger.info(f"Response received for url: {url}")
                break
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Exception occurred: {e}")
                self.logger.error(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

        return success

    def process_data(self, data):
        raise NotImplementedError("Subclasses must implement the process_data method.")

    def convert_values_to_float(self, input_data):
        def convert_value(value):
            if isinstance(value, str):
                value = value.replace(",", "")
                try:
                    value = float(value)
                except ValueError:
                    if value == '-':
                        value = None
                    # If conversion fails, leave the value unchanged
                    pass
            return value

        if isinstance(input_data, dict):
            converted_data = {}
            for key, value in input_data.items():
                converted_data[key] = convert_value(value)
            return converted_data
        elif isinstance(input_data, list):
            converted_data = []
            for item in input_data:
                converted_data.append(convert_value(item))
            return converted_data
        else:
            raise ValueError("Input data must be a dictionary or a list")

    def cleanup_logs_folder(self, name):
        # Construct the full path to the folder
        current_directory = os.getcwd()

        # Add "logs" folder to the current directory path
        folder_path = os.path.join(current_directory, "logs")
        # Check if the folder exists
        if not os.path.exists(folder_path):
            self.logger.error(f"Folder '{folder_path}' does not exist.")
            return

        # Iterate over all items in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            # Check if the item is a directory and if its name matches the specified name
            if os.path.isdir(item_path) and name in item:
                # Get list of files in the directory
                files = [os.path.join(item_path, f) for f in os.listdir(item_path) if
                         os.path.isfile(os.path.join(item_path, f))]
                # Sort files by modification time
                files.sort(key=os.path.getmtime)
                # Delete all files except the most recent 500
                files_to_delete = files[:-500]
                for file_to_delete in files_to_delete:
                    try:
                        os.remove(file_to_delete)
                        self.logger.info(f"Deleted file: {file_to_delete}")
                    except Exception as e:
                        self.logger.error(f"Error deleting file: {file_to_delete}, {e}")
