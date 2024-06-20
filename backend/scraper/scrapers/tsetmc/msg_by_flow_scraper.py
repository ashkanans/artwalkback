import socket
import time
from threading import Thread

import jsonpickle

from backend.engine.socket_log import SocketLog
from backend.engine.update.TaskStatus import TaskStatus
from backend.scraper.scrapers.base_scraper import BaseScraper
from backend.scraper.tsetmc.service.msg_by_flow_service import MsgByFlowService


class MsgByFlowScraper(BaseScraper):
    def __init__(self, ip='192.168.1.108', port= 9090):
        super(MsgByFlowScraper, self).__init__()
        self.progress_socket = socket.socket()
        self.create_socket_connection(9090)
        self.socket_log = SocketLog("MsgByFlow", TaskStatus.PENDING, 0, -1)


    def create_socket_connection(self, port):
        try:
            self.progress_socket = socket.socket()
            self.progress_socket.connect(("192.168.1.108", port))
        except Exception as e:
            print(f"Error creating connection: {e}")

    def send_progress(self):
        self.create_socket_connection(9090)

        try:
            json_string = jsonpickle.encode(self.socket_log)
            self.progress_socket.send(json_string.encode())
            message = self.progress_socket.recv(1024)
            message = message.decode()
            self.progress_socket.close()
        except Exception as e:
            print(f"Error creating table: {e}")

    def process_data(self, json_data):
        msg_by_flow_data = json_data.get("msg", [])
        self.socket_log.status = TaskStatus.PROCESS_DATA
        self.socket_log.progress = 0
        self.socket_log.total = len(msg_by_flow_data)
        self.send_progress()
        if msg_by_flow_data:
            self.socket_log.status = TaskStatus.SAVING_DATA
            self.send_progress()
            msg_by_flow_service = MsgByFlowService()

            if not msg_by_flow_service.table_exists():
                msg_by_flow_service.create_table()
                self.logger.info("Created table: tse_msg_by_flow")
            for msg in msg_by_flow_data:
                msg_by_flow_service.update_msg_by_flow(msg)
                self.socket_log.progress += 1
                self.send_progress()

            self.socket_log.status = TaskStatus.COMPLETED
            self.send_progress()
            self.logger.info("MsgByFlow data retrieved successfully.")
        else:
            self.logger.warning("MsgByFlow data could not be retrieved.")

        self.progress_socket.close()