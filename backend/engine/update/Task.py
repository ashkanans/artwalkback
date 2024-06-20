import tkinter as tk

from backend.engine.socket_log import SocketLog


class Task:
    def __init__(self, name, frequency, parent):
        self.isParent = parent
        self.name = name
        self.frequency = frequency
        self.checkbox_var = tk.BooleanVar()
        self.selected = False
        self.children = []
        self.progress = SocketLog
