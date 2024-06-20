import importlib
import json
import logging
import os
import socket
from concurrent.futures import ThreadPoolExecutor

import jsonpickle
from apscheduler.schedulers.background import BackgroundScheduler

from backend.engine.socket_log import SocketLog
from backend.engine.update.TaskStatus import TaskStatus
from backend.scraper.scrapers.url_builder.url import UrlBuilder


class ScraperManager:
    def __init__(self, config_path='', ip='localhost', port=9090):
        # self.listeners = []
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        self.executor = ThreadPoolExecutor(max_workers=max(1, os.cpu_count() - 2))
        self.scheduler = BackgroundScheduler()
        self.socket_log = None
        if config_path:
            with open(config_path, 'r', encoding='utf-8') as config_file:
                self.config = json.load(config_file)

        self.ip = ip
        self.port = port

    # def add_listener(self, listener):
    #     self.listeners.append(listener)

    # def on_start(self, data):
    #     for listener in self.listeners:
    #         listener.handle_on_start(data)

    # def on_finished(self, data):
    #     for listener in self.listeners:
    #         listener.handle_on_finished(data)

    def snake_case(self, name):
        """
        Convert CamelCase to snake_case.
        """
        return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')

    def create_scraper(self, scraper_info):
        try:
            scraper_name = scraper_info.get('name')
            site_name = scraper_info.get('siteName')

            module_name = self.snake_case(scraper_name)

            scraper_module = importlib.import_module(f'backend.scraper.scrapers.{site_name}.{module_name}_scraper')
            scraper_class = getattr(scraper_module, f"{scraper_name}Scraper")

            self.logger.info(f"Created {scraper_name}Scraper successfully.")

            url_builder = UrlBuilder(scraper_info.get('siteName'))

            urls, ids = url_builder.create_full_url(scraper_info)

            scraper_info["urls"] = urls
            scraper_info["ids"] = ids

            sc = scraper_class(self.ip, self.port)
            sc.add_config(scraper_info)

            return sc

        except Exception as e:
            self.logger.error(f"Error creating scraper: {e}")
            raise e

    def run_specific_scraper(self, scraper_name):
        scraper_info_list = [d for d in self.config.get('requests_urls', []) if d.get('name') == scraper_name]

        for scraper_info in scraper_info_list:
            scraper = self.create_scraper(scraper_info)
            scraper.fetch_data_from_urls()

        # # Schedule scraper jobs
        # self.schedule_scraper_jobs(scraper_name)
        #
        # # Start the scheduler in a separate thread
        # self.executor.submit(self.start_scheduler)
        # self.executor.shutdown(wait=True)

    def run_specific_scraper_majid(self, scraper_info):
        # self.socket_log = SocketLog("")
        # self.on_start(scraper_info)
        scraper = self.create_scraper(scraper_info)
        scraper.cleanup_logs_folder(scraper.config.get('name'))

        # scraper.add_listener(self)
        scraper.fetch_data_from_urls()
        # self.on_finished(scraper_info)

        # # Schedule scraper jobs
        # self.schedule_scraper_jobs(scraper_name)
        #
        # # Start the scheduler in a separate thread
        # self.executor.submit(self.start_scheduler)
        # self.executor.shutdown(wait=True)

    def run_all_scrapers(self):
        for scraper_info in self.config.get('requests_urls', []):
            scraper = self.create_scraper(scraper_info)
            scraper.fetch_data_from_urls()

        # Start the scheduler in a separate thread
        self.executor.submit(self.start_scheduler)

        # Keep the main thread alive
        try:
            while True:
                pass
        except KeyboardInterrupt:
            # Stop the scheduler (if the program is interrupted)
            self.scheduler.shutdown()

    def run_scraper_job(self, scraper_info):
        scraper = self.create_scraper(scraper_info)
        scraper.fetch_data_from_urls()

    def schedule_scraper_jobs(self, scraper_name):
        scraper_info_list = [d for d in self.config.get('requests_urls', []) if d.get('name') == scraper_name]
        for scraper_info in scraper_info_list:
            # Schedule the job to run every X seconds (adjust as needed)
            self.scheduler.add_job(self.run_scraper_job, 'interval', args=[scraper_info], seconds=5)

    def start_scheduler(self):
        try:
            # Start the scheduler
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            # Stop the scheduler (if the program is interrupted)
            self.scheduler.shutdown()
