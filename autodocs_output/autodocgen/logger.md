# autodocgen/logger.py

> **Summary of Python File: Simple Logger**

This Python file defines a class `SimpleLogger` that creates a simple logging system. 

### Key Features:

*   The logger logs messages with an `INFO` level or higher.
*   Logs are output to both the console and a log file (`app.log` by default).
*   The log format includes the timestamp (`%(asctime)s`) and the log message (`%(message)s`).
*   The logger can be customized with a name and log file when creating an instance of `SimpleLogger`.

### Usage:

To use this logger, you can create an instance of the `SimpleLogger` class and call it with a message. For example:

```python
logger = SimpleLogger()
logger("This is a log message")
```

This will log the message to both the console and the log file.


---


## Class: `SimpleLogger`

No class docstring available.


### Method: `__init__`
- **Arguments**: ['self', 'name', 'log_file']
- **Returns**: None

Initializes a SimpleLogger instance with a specified name and log file.

Args:
    name (str): The name of the logger, defaults to my_logger.
    log_file (str): The file where logs will be written, defaults to app.log.

### Method: `__call__`
- **Arguments**: ['self', 'message']
- **Returns**: None

Makes a call to the logger with a given message, utilizing the SimpleLogger instance's configured logging settings. 

Args:
    message (str): The message to be logged by the SimpleLogger instance.

Returns:
    None



