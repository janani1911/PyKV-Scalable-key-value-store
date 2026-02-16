import json
import os
from collections import OrderedDict

class PyKVStore:
    def __init__(self, capacity=5, file_path="data/pkv_data.json"):
        self.capacity = capacity
        self.file_path = file_path
        self.store = OrderedDict()
        self._load_from_disk()

    # ---------- SET ----------
    def set(self, key, value):
        if key in self.store:
            self.store.pop(key)

        elif len(self.store) >= self.capacity:
            self.store.popitem(last=False)  # LRU eviction

        self.store[key] = value
        self._save_to_disk()

    # ---------- GET ----------
    def get(self, key):
        if key not in self.store:
            return None

        self.store.move_to_end(key)
        self._save_to_disk()
        return self.store[key]

    # ---------- DELETE ----------
    def delete(self, key):
        if key in self.store:
            del self.store[key]
            self._save_to_disk()
            return True
        return False

    # ---------- SHOW ALL ----------
    def all(self):
        return {
            "data": dict(self.store),
            "lru_order": list(self.store.keys()),
            "capacity": self.capacity,
            "current_size": len(self.store)
        }

    # ---------- DISK ----------
    def _save_to_disk(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as f:
            json.dump(self.store, f)

    def _load_from_disk(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.store = OrderedDict(data)
