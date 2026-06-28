import os
import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


WATCH_EXTENSIONS = {".py", ".kv"}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    ".kivy",
    "logs",
    "build",
    "bin"
}

RESTART_DELAY = 0.75


class DevRunner(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.last_restart = 0
        self.restart_count = 0
        self.start_time = 0

        self.start_app()

    def start_app(self):

        self.restart_count += 1

        self.start_time = time.perf_counter()

        os.system("cls" if os.name == "nt" else "clear")

        if os.name == "nt":
            os.system("title AKM Finance Manager - Development")

        print("=" * 60)
        print("AKM Finance Manager")
        print("Development Mode")
        print("=" * 60)

        print(f"Launch #{self.restart_count}\n")

        self.process = subprocess.Popen(
            [sys.executable, "main.py"]
        )

        elapsed = time.perf_counter() - self.start_time

        print(f"Started in {elapsed:.2f}s\n")

    def stop_app(self):
        if self.process is None:
            return

        if self.process.poll() is None:
            print("\n🛑 Stopping application...\n")

            self.process.terminate()

            try:
                self.process.wait(timeout=5)

            except subprocess.TimeoutExpired:
                print("Application did not exit. Killing...")
                self.process.kill()
                self.process.wait()

        self.process = None

    def restart_app(self):
        now = time.time()

        if now - self.last_restart < RESTART_DELAY:
            return

        self.last_restart = now

        print("\n🔄 Source change detected")

        self.stop_app()

        self.start_app()

    def on_modified(self, event):

        if event.is_directory:
            return

        path = Path(event.src_path)

        if any(
            part in IGNORED_DIRECTORIES
            for part in path.parts
        ):
            return

        if path.suffix.lower() not in WATCH_EXTENSIONS:
            return

        if path.name.endswith("~"):
            return

        if path.name.endswith(".tmp"):
            return

        if path.name.endswith(".pyc"):
            return

        print(f"\n File Changed: {path}")

        self.restart_app()


def main():

    handler = DevRunner()

    observer = Observer()

    observer.schedule(
        handler,
        ".",
        recursive=True
    )

    observer.start()

    print("Watching project for changes...")
    print("Press Ctrl+C to exit.\n")

    try:

        while True:

            if handler.process is not None:

                if handler.process.poll() is not None:
                    handler.process = None

            time.sleep(0.2)

    except KeyboardInterrupt:

        print("\nStopping development server...")

        observer.stop()

        handler.stop_app()

    observer.join()


if __name__ == "__main__":
    main()