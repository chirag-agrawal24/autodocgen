import logging


class SimpleLogger:
    """SimpleLogger class description."""

    def __init__(self, name='my_logger', log_file='app.log'):
        """Initializes an instance with the given name and log file.
 
Parameters:
    name (str): The name of the instance.
    log_file (str): The path to the log file."""
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
        """Invokes the instance with a given message when an AI summary fails. 
Parameters:
  self: A reference to the instance of the class.
  message: The message associated with the AI summary failure."""
        self.logger.info(message)
