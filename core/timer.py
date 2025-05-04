from time import perf_counter

class Timer:
    def __init__(self):
        self.start_time = perf_counter()

    def elapsed(self) -> float:
        return perf_counter() - self.start_time
