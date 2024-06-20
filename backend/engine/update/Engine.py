import datetime
import multiprocessing
import os
import threading
import time  # for dummy execution time
import tkinter as tk
import tkinter.font as tkFont
import socket
from tkinter import ttk

import jsonpickle
import psutil  # for dummy resource usage

from backend.engine.socket_log import SocketLog
from backend.engine.update.JobManager import JobManager
from backend.engine.update.TaskManager import TaskManager


class Engine:
    def __init__(self, root):
        self.execution_history_text = tk.Text()
        self.history_text = ""
        self.status_indicator = tk.Label(root, text="")
        self.progress_bar = ttk.Progressbar()
        self.progress_var = tk.DoubleVar()
        self.list_task_ids = {}
        self.process_events = {}
        self.job_manager_list = []
        self.log_tabs = {}
        self.right_panel = None
        self.paned_window = None
        self.left_panel = None
        self.tree = None
        self.root = root
        self.root.title("ESTDCO Capital Marketing Dashboard Engine")
        self.root.geometry("800x600")

        self.server_socket = None
        self.all_threads = []
        self.host = '192.168.1.108'
        self.port = 9090
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icons8-engine-34.ico")

        self.root.iconbitmap(icon_path)

        icon_path = os.path.join(script_dir, "icons8-engine-34.png")
        taskbar_icon = tk.PhotoImage(file=icon_path)
        self.root.wm_iconphoto(True, taskbar_icon)

        self.task_manager = TaskManager()
        self.task_manager.load_tasks()

        self.create_ui()
        t = threading.Thread(target=self.open_socket)
        t.start()

    def open_socket(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket = socket.socket()
        # self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        try:
            while True:
                print("Waiting for client")
                conn, addr = self.server_socket.accept()

                print("Client:", addr)

                t = threading.Thread(target=self.start_listen, args=(conn, addr))
                t.start()

                self.all_threads.append(t)
        except KeyboardInterrupt:
            print("Stopped by Ctrl+C")
        finally:
            if self.server_socket:
                self.server_socket.close()
            for t in self.all_threads:
                t.join()

    def start_listen(self, conn, addr):
        # recv message
        message = conn.recv(1024)
        # message = message.decode()
        obj = jsonpickle.decode(message)
        self.update_progress(obj)
        # send answer
        message = "Ok"
        message = message.encode()
        conn.send(message)
        conn.close()


    def create_ui(self):
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.left_panel = ttk.Frame(self.paned_window, width=200)
        self.paned_window.add(self.left_panel)

        self.right_panel = ttk.Notebook(self.paned_window)
        self.paned_window.add(self.right_panel)

        self.tree = ttk.Treeview(self.left_panel, columns=("Task Name", "Update Frequency", "Checkbox"),
                                 show="headings")
        self.tree.heading("Task Name", text="Task Name", anchor=tk.CENTER)
        self.tree.heading("Update Frequency", text="Update Frequency (s)", anchor=tk.CENTER)
        self.tree.heading("Checkbox", text="Checkbox", anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.tag_configure("parent", background="light blue")

        parent_id = None
        for task in self.task_manager.task_checkboxes:
            if task.isParent:
                parent_id = self.tree.insert("", "end", values=(task.name, task.frequency, ""),
                                             tags=("parent", task.name))
                self.list_task_ids[parent_id] = task.name
            else:
                child_id = self.tree.insert(parent_id, "end", values=(task.name, task.frequency, ""), tags=task.name)
                self.list_task_ids[child_id] = task.name

        start_button = tk.Button(self.left_panel, text="Start Selected Tasks", command=self.start_button_click)
        start_button.pack(side=tk.LEFT, pady=5, padx=5)

        force_end_button = tk.Button(self.left_panel, text="Force End", command=self.force_end)
        force_end_button.pack(side=tk.LEFT, pady=5, padx=5)

        for column in ("Task Name", "Update Frequency", "Checkbox"):
            header_width = tkFont.Font().measure(column)
            max_content_width = max(
                tkFont.Font().measure(self.tree.set(child, column))
                for child in self.tree.get_children("")
            )
            self.tree.column(column, width=max(header_width, max_content_width), anchor=tk.CENTER)

        self.attach_checkbox_toggle(self.tree)

    def attach_checkbox_toggle(self, tree):
        self.tree.bind("<Button-1>", lambda event: self.on_checkbox_clicked(event))

    def on_checkbox_clicked(self, event):
        # Identify the column clicked
        col = self.tree.identify_column(event.x)

        # Check if the clicked column is the "Checkbox" column
        if col == "#3":
            selected_item_id = self.tree.selection()
            self.toggle_checkbox(selected_item_id)

    def find_index_of_value(self, dictionary, target_value):
        for index, (key, value) in enumerate(dictionary.items()):
            if value == target_value:
                return index
        return -1  # If the target value is not found

    def toggle_checkbox(self, selected_item_id):
        if selected_item_id:
            item_id = selected_item_id[0]

            task_name = self.list_task_ids[item_id]

            task = [d for d in self.task_manager.task_checkboxes if d.name == task_name][0]

            # If it's a parent, toggle its state and its children
            if task.isParent:
                new_state = "1" if not task.selected else "0"
                self.tree.set(item_id, "Checkbox", new_state)
                task.selected = not task.selected
                child_indexes = self.tree.get_children(item_id)
                for child_index in child_indexes:
                    child_task_name = self.list_task_ids[child_index]
                    child_task = [d for d in self.task_manager.task_checkboxes if d.name == child_task_name][0]
                    self.tree.set(child_index, "Checkbox", new_state)
                    child_task.selected = task.selected

            else:
                # Toggle the state of the child only
                new_state = "1" if not task.selected else "0"
                self.tree.set(item_id, "Checkbox", new_state)
                task.selected = not task.selected

            # If all children of a parent are selected, select the parent
            parent_id = self.tree.parent(item_id)
            if parent_id:
                parent_task_name = self.list_task_ids[parent_id]
                parent_task = [d for d in self.task_manager.task_checkboxes if d.name == parent_task_name][0]
                children_selected = all(child_task.selected for child_task in parent_task.children)
                self.tree.set(parent_id, "Checkbox", "1" if children_selected else "0")
                parent_task.selected = children_selected

    def force_end(self):
        selected = self.get_selected_checkboxes()
        for task in selected:
            for tab_name, log_text in self.log_tabs.items():
                if tab_name == task[0]:
                    pass
                    # self.right_panel.forget(log_text)  # Remove log text from display
            event_to_be_set = self.process_events[task[0]]
            if event_to_be_set:
                event_to_be_set.set()

    def start_button_click(self, log_tabs=None):
        selected = self.get_selected_checkboxes()
        update_frequency = None
        executed_child_task = None
        scrape_type = None

        for task in selected:
            executed_task = [d for d in self.task_manager.scraper_list if d.get('scraper_type') == task[0]]
            for scraper_list in self.task_manager.scraper_list:
                if scraper_list.get("requests_urls"):
                    for request_url in scraper_list.get("requests_urls"):
                        if request_url.get("name") == task[0]:
                            update_frequency = scraper_list.get('update_frequency')
                            scrape_type = scraper_list.get('scraper_type')
                            executed_child_task = request_url

            tab = ttk.Frame(self.right_panel)
            self.right_panel.add(tab, text=task[0])

            # Create a PanedWindow for the tab and split it vertically
            tab_paned_window = ttk.PanedWindow(tab, orient=tk.VERTICAL)
            tab_paned_window.pack(fill=tk.BOTH, expand=True)

            # Top half of the tab
            top_pane = ttk.Frame(tab_paned_window)
            tab_paned_window.add(top_pane)

            # Widgets for task status, progress bar, execution time, resource usage, execution history

            # Dummy values for demonstration purposes
            dummy_frame = ttk.Frame(top_pane)
            dummy_frame.pack(pady=10)

            dummy = tk.Label(dummy_frame, text="Under Development. Seeing Dummy values (for now!)",
                             font=("Helvetica", 12, "bold"))
            dummy.grid(row=0, column=0, padx=5, sticky="w")

            status_frame = ttk.Frame(top_pane)
            status_frame.pack(pady=10)

            task_status_label = tk.Label(status_frame, text="Task Status:", font=("Helvetica", 12, "bold"))
            task_status_label.grid(row=0, column=0, padx=5, sticky="w")

            self.status_indicator = tk.Label(status_frame, text="PENDING", fg="green")
            self.status_indicator.grid(row=0, column=1, padx=5, sticky="w")

            progress_frame = ttk.Frame(top_pane)
            progress_frame.pack(pady=10)

            progress_label = tk.Label(progress_frame, text="Progress:", font=("Helvetica", 12, "bold"))
            progress_label.grid(row=0, column=0, padx=5, sticky="w")

            self.progress_var = tk.DoubleVar()
            self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=200, mode='determinate',
                                           variable=self.progress_var)
            self.progress_bar.grid(row=0, column=1, padx=5, sticky="w")
            self.progress_var.set(0)  # Set progress to 50% for demonstration

            exec_frame = ttk.Frame(top_pane)
            exec_frame.pack(pady=10)

            start_time = time.time()  # Start time of the task
            execution_time_label = tk.Label(exec_frame,
                                            text=f"Start Time: {time.strftime('%H:%M:%S', time.gmtime(start_time))}",
                                            font=("Helvetica", 12, "bold"))
            execution_time_label.grid(row=0, column=0, padx=5, sticky="w")

            # Dummy resource usage
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            resource_usage_label = tk.Label(exec_frame,
                                            text=f"Resource Usage: CPU {cpu_percent}% | Memory {memory_percent}%",
                                            font=("Helvetica", 12, "bold"))
            resource_usage_label.grid(row=0, column=1, padx=5, sticky="w")

            next_execution_label = tk.Label(exec_frame,
                                            text=f"Next Scheduled Execution: {datetime.datetime.now() + datetime.timedelta(hours=1)}",
                                            font=("Helvetica", 12, "bold"))
            next_execution_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

            hist_frame = ttk.Frame(top_pane)
            hist_frame.pack(pady=10)

            execution_history_label = tk.Label(hist_frame, text="Execution History:", font=("Helvetica", 12, "bold"))
            execution_history_label.grid(row=0, column=0, padx=5, sticky="w")

            self.history_text = ""
            self.execution_history_text = tk.Text(hist_frame, height=5, width=50)
            self.execution_history_text.insert(tk.END, self.history_text)
            self.execution_history_text.grid(row=1, column=0, padx=5, sticky="w")

            # Bottom half of the tab
            bottom_pane = ttk.Frame(tab_paned_window)
            tab_paned_window.add(bottom_pane)

            # Text widget to display console output
            console_output = tk.Text(bottom_pane)
            console_output.pack(fill=tk.BOTH, expand=True)

            log_text = tk.Text(tab)
            log_text.pack(fill=tk.BOTH, expand=True)
            self.log_tabs[task[0]] = log_text

            try:
                if executed_task:
                    for task in executed_task:
                        update_frequency = task.get('update_frequency')
                        requests_urls = task.get('requests_urls')
                        scrape_type = task.get('scraper_type')
                        event = multiprocessing.Event()
                        self.process_events[scrape_type] = event
                        for request in requests_urls:
                            job_manager = JobManager(request, update_frequency, scrape_type, request.get('name'), event)
                            self.job_manager_list.append(job_manager)
                            job_manager.start()

                elif executed_child_task:
                    event = multiprocessing.Event()
                    self.process_events[executed_child_task.get('name')] = event

                    job_manager = JobManager(executed_child_task, update_frequency, scrape_type,
                                             executed_child_task.get('name'), event, self.port)
                    self.job_manager_list.append(job_manager)
                    job_manager.start()


            except Exception as e:
                print("An error occurred:", e)

    def get_selected_checkboxes(self):
        selected = []
        for task in self.task_manager.task_checkboxes:
            if task.selected:
                selected.append((task.name, task.frequency))
        return selected

    def update_progress(self, socket_log: SocketLog):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        filtered_tasks = [task for task in self.task_manager.task_checkboxes if task.name == socket_log.name]
        if filtered_tasks:
            filtered_tasks[0].progress = socket_log

        self.status_indicator.config(text=socket_log.status.name)
        self.progress_bar['maximum'] = socket_log.total
        self.progress_var.set(socket_log.progress)
        self.history_text += f"\n{formatted_datetime} - {socket_log.status.name}"
        self.execution_history_text.insert(tk.END, self.history_text)
