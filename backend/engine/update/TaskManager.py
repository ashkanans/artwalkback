from backend.engine.update.ConfigLoader import ConfigLoader
from backend.engine.update.Task import Task


class TaskManager:
    def __init__(self):
        self.scraper_list = None
        self.task_checkboxes = []

    def load_tasks(self):
        self.scraper_list = ConfigLoader().load_configs()

        for config in self.scraper_list:
            if 'scraper_type' in config and 'update_frequency' in config:
                task_parent = Task(config['scraper_type'], config['update_frequency'], parent=True)
                self.task_checkboxes.append(task_parent)
                request_urls = config.get('requests_urls')
                for request in request_urls:
                    task_child = Task(request.get("name"), "", parent=False)
                    self.task_checkboxes.append(task_child)
                    task_parent.children.append(task_child)
