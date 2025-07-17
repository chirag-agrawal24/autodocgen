import logging


class SimpleLogger:
    """SimpleLogger class description."""

    def __init__(self, name='my_logger', log_file='app.log'):
        """Initializes the class instance with a name and log file.

Args:
    name (str): The name of the instance.
    log_file (str): The path to the log file.

Returns:
    None"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            fh = logging.FileHandler(log_file, mode='w', encoding='utf-8')
            fh.setLevel(logging.INFO)
            fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)

    def __call__(self, message):
        """Handles AI summary failure by processing the provided message, typically triggering an error response or fallback behavior to handle the unsuccessful summarization attempt."""
        self.logger.info(message)
