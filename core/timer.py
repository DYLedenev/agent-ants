from time import perf_counter

class Timer:
    """A simple timer class for measuring elapsed time.
    
    This class provides functionality to measure elapsed time from when the timer
    was initialized.
    """
    def __init__(self):
        """Initialize a new Timer instance.
        
        The timer starts automatically upon initialization.
        """
        self.start_time = perf_counter()

    def elapsed(self) -> float:
        """Calculate the elapsed time since the timer was started.
        
        Returns:
            float: The elapsed time in seconds
        """
        return perf_counter() - self.start_time
