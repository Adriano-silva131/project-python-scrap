import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from main import main


class FolderWatcher(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory

    def on_created(self, event):
        if not event.is_directory:
            print(f"Novo arquivo adicionado: {event.src_path}")
            main(self.directory)


def start_folder_watcher(directory):
    event_handler = FolderWatcher(directory)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    return observer
