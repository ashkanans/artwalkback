import socket
from datetime import datetime

import jsonpickle

from backend.engine.socket_log import SocketLog
from backend.engine.update.TaskStatus import TaskStatus
from backend.scraper.scraper_manager import ScraperManager


class JobFunctions:
    def __init__(self):
        self.listeners = []
        self.socket_log = None
        self.ip = '192.168.1.108'
        self.port = 9090
        self.progress_socket = socket.socket()
        self.socket_log = SocketLog("", TaskStatus.PENDING, 0, -1)
        self.create_socket_connection()
    # def add_listener(self, listener):
    #     self.listeners.append(listener)
    #
    # def remove_listener(self, listener):
    #     self.listeners.remove(listener)

    # def on_start(self, data):
    #     json_string = jsonpickle.encode(self.socket_log)
    #     for listener in self.listeners:
    #         listener.handle_on_start(json_string)
    #
    # def on_finished(self, data):
    #     for listener in self.listeners:
    #         listener.handle_on_finished(data)
    #
    # def on_exception(self, data):
    #     for listener in self.listeners:
    #         listener.handle_on_exception(data)

    # def handle_on_start(self, data):
    #     self.on_start(data)
    #
    # def handle_on_finished(self, data):
    #     self.on_finished(data)
    def create_socket_connection(self):
        try:
            self.progress_socket = socket.socket()
            self.progress_socket.connect((self.ip, self.port))
        except Exception as e:
            print(f"Error creating connection: {e}")

    def send_progress(self, status: TaskStatus, progress: int, total: int):

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

    def start_job(self, requests_url):
        self.socket_log.name = requests_url['name']

        self.send_request(requests_url)
        # print(f"{datetime.now()} started. request url count: {len(requests_urls)} ")
        # start_time = time.time()
        # with multiprocessing.Pool(processes=len(requests_urls)) as pool:
        #     pool.map(self.send_request, requests_urls)
        # end_time = time.time()
        # execution_time = end_time - start_time
        # print(f"{datetime.now()} job_cbi count({len(requests_urls)}) finished. Execution time: {execution_time}.")

    def send_request(self, requests_url):
        try:
            scraper_name = requests_url['name']
            if scraper_name:
                print(f"{datetime.now()} {scraper_name} scraper started.")
                manager = ScraperManager('', self.ip, self.port)
                # manager.add_listener(self)
                # self.socket_log = SocketLog(scraper_name, TaskStatus.STARTED, 0, 100)
                # self.on_start(requests_url)
                self.send_progress(TaskStatus.STARTED, 0, 90)
                manager.run_specific_scraper_majid(requests_url)
                self.send_progress(TaskStatus.COMPLETED, 0, 90)

                # url = f"{request_info['BaseUrl']}{request_info['url']}"
                # response = requests.request(request_info['requestMethod'], url)
                print(f"{datetime.now()} {scraper_name} scraper finished.")
        except Exception as e:
            # self.on_exception(requests_url)
            print(f"{datetime.now()} Failed to send request to {requests_url['url']}: {str(e)}")
