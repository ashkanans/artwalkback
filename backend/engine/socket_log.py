import jsonpickle

from backend.engine.update.TaskStatus import TaskStatus


class SocketLog:
    def __init__(self, name: str, status: TaskStatus, progress: int, total: int):
        self.name = name
        self.status = status
        self.progress = progress
        self.total = total

