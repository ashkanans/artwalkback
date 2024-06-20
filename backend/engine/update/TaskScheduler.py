import time

import schedule


class TaskScheduler:
    def __init__(self):
        self.schedule = schedule.Scheduler()

    def schedule_task(self, update_frequency, job_manager, requests_urls):
        """
        Schedule a task with given update frequency and job manager.

        Parameters:
        - update_frequency: The frequency of the task in seconds.
        - job_manager: An instance of JobFunctions.
        - requests_urls: List of URLs for the task.
        """
        if update_frequency is None:
            print("No update frequency specified.")
        else:
            update_frequency = int(update_frequency)
            if update_frequency > 0:
                self.schedule.every(update_frequency).seconds.do(job_manager.start_job, requests_urls)
                while True:
                    self.schedule.run_pending()
                    time.sleep(1)
