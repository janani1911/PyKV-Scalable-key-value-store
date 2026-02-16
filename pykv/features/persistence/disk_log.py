import os
from config import LOG_FILE

class DiskPersistence:

    def log_set(self, key, value):
        with open(LOG_FILE, "a") as f:
            f.write(f"SET {key} {value}\n")

    def log_delete(self, key):
        with open(LOG_FILE, "a") as f:
            f.write(f"DEL {key}\n")

    def recover(self, store):
        if not os.path.exists(LOG_FILE):
            return

        with open(LOG_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 2)
                if parts[0] == "SET":
                    store.set(parts[1], parts[2], persist=False)
                elif parts[0] == "DEL":
                    store.delete(parts[1], persist=False)
