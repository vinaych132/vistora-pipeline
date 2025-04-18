import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = r"C:\Users\Vinay\Documents\MyProject\vistora-pipeline"

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"[+] Change detected: {event.src_path}")
        commit_and_push()

def commit_and_push():
    os.chdir(WATCH_DIR)
    subprocess.run(["git", "add", "."], shell=True)
    subprocess.run(["git", "commit", "-m", "Auto: update on file change"], shell=True)
    subprocess.run(["git", "push", "origin", "main"], shell=True)
    print("[✓] Auto push complete")

if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=True)
    observer.start()
    print("[*] Watching for changes... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()