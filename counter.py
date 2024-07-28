class Counter:
    def __init__(self):
        self.count = 0
        self.is_open = True

    def add(self):
        if not self.is_open:
            raise Exception("Counter is closed")
        self.count += 1

    def get_count(self):
        return self.count

    def close(self):
        self.is_open = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()