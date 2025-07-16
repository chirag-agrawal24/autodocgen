# autodocgen/logger.py

> **Summary:**

This Python file defines a simple logger class called `SimpleLogger`. The logger is designed to log messages to both the console and a file.

**Key Features:**

* Logs messages at the `INFO` level
* Writes logs to both the console and a file (default file name is `app.log`)
* Logs are formatted with a timestamp and the log message
* The logger can be instantiated with a custom name and log file name

**Usage:**

To use this logger, you would create an instance of the `SimpleLogger` class and call it with a message to log:
```python
logger = SimpleLogger()
logger("This is a log message")
```
This would output the log message to both the console and the log file.

**Notes:**

* The logger uses the Python `logging` module, which is a built-in module.
* The logger propagates logs to parent loggers, but this is explicitly disabled in this implementation (`self.logger.propagate = False`).
* The log file is opened in write mode (`mode='w'`), which means that existing logs will be overwritten. If you want to append to the log file instead, change this to `mode='a'`.


---


## Class: `SimpleLogger`

No class docstring available.


### Method: `__init__`
- **Arguments**: ['self', 'name', 'log_file']
- **Returns**: None

Initializes a SimpleLogger instance with a configurable name and log file.

  name (str): The name of the logger (default: 'my_logger')
  log_file (str): The file path for logging (default: 'app.log')

### Method: `__call__`
- **Arguments**: ['self', 'message']
- **Returns**: None

Logs a given message using the configured logger.

 
Parameters
----------
self : SimpleLogger
    The instance of SimpleLogger.
message : str
    The message to be logged.



