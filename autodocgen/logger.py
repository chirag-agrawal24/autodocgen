import logging

class SimpleLogger:
    def __init__(self, name='my_logger', log_file='app.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        if not self.logger.handlers:
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

            # File handler with UTF-8
            fh = logging.FileHandler(log_file, mode='w', encoding='utf-8')
            fh.setLevel(logging.INFO)
            fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

            self.logger.addHandler(ch)
            self.logger.addHandler(fh)

    def __call__(self, message):
        self.logger.info(message)
