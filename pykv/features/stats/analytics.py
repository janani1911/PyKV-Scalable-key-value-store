class StoreStats:
    def __init__(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.set_ops = 0
        self.get_ops = 0
        self.delete_ops = 0

    def hit(self):
        self.cache_hits += 1

    def miss(self):
        self.cache_misses += 1

    def snapshot(self, total_keys, capacity):
        return {
            "total_keys": total_keys,
            "capacity": capacity,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "set_ops": self.set_ops,
            "get_ops": self.get_ops,
            "delete_ops": self.delete_ops
        }
