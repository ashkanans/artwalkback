import multiprocessing
import socket
import time
from multiprocessing import Process

from backend.engine.update.JobFunctions import JobFunctions
from backend.engine.update.TaskScheduler import TaskScheduler


class JobManager(Process):
    def __init__(self, request_url, update_frequency, scrape_type, name, event, port):
        super().__init__()
        # self.progress_socket = socket.socket()
        # self.progress_socket.connect(("localhost", port))
        # message = "Hello"
        # print('send:', message)
        # message = message.encode()
        # self.progress_socket.send(message)


        self.event = event
        self.lock = multiprocessing.Lock()
        self.job = None
        self.request_url = request_url
        self.update_frequency = int(update_frequency)
        self.scraper_type = scrape_type

        self.has_error = False
        self.job_manager = JobFunctions()
        self.task_scheduler = TaskScheduler()

        self.job = self.add_job(self.update_frequency, self.job_manager.start_job, self.request_url)
        super().__init__(name=name, args=(event,))

    def run(self):

        if not self.update_frequency:
            print("No update frequency")
        else:

            if self.update_frequency > 0:

                while True:

                    if self.event.is_set():
                        self.task_scheduler.schedule.cancel_job(self.job)  # Cancel the scheduled job
                        break  # Exit the loop to stop the script
                    self.task_scheduler.schedule.run_pending()

                    time.sleep(1)


    # def handle_on_start(self, data):
    #     self.progress_socket.send(data)
    #
    # def handle_on_finished(self, data):
    #     self.progress_socket.send(data)
    #
    # def handle_on_exception(self, data):
    #     self.has_error = True
    #     # self.remove_current_job()
    #     print("Event handled on exception:", data)

    def add_job(self, update_frequency, job_function, *args, **kwargs):
        """
        Add a job to the scheduler.

        Parameters:
        - update_frequency: The frequency at which the job should run.
        - job_function: The function to be executed as the job.
        - *args, **kwargs: Additional arguments to pass to the job function.

        Returns:
        - The job object.
        """
        # self.job_manager.add_listener(self)
        job = self.task_scheduler.schedule.every(update_frequency).seconds.do(job_function, *args, **kwargs)
        return job

    def remove_current_job(self):
        """
        Remove a job from the scheduler.

        Parameters:
        - job: The job object to remove.
        """
        with self.lock:
            self.task_scheduler.schedule.cancel_job(self.job)
