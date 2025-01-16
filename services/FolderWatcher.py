import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from main import main


class FolderWatcher(FileSystemEventHandler):
    def __init__(self, directory, callback):
        super().__init__()
        self.directory = directory
        self.callback = callback
        self.processed_files = {} 

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def process_file(self, file_path):
        modification_time = os.path.getmtime(file_path)

        if (
            file_path not in self.processed_files
            or self.processed_files[file_path] < modification_time
        ):
            self.processed_files[file_path] = modification_time
            self.callback(file_path)


def start_folder_watcher(directory, callback):
    event_handler = FolderWatcher(directory, callback)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    return observer
