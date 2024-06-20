from enum import Enum


class TaskStatus(Enum):
    STARTED = 0
    FETCHING_DATA = 1
    PROCESS_DATA = 2
    SAVING_DATA = 3
    EXCEPTION = 4
    PENDING = 5
    IN_PROGRESS = 6
    COMPLETED = 7
    BLOCKED = 8
    CANCELLED = 9
