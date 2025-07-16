# autodocgen/logger.py

> **Simple Logger Class Summary**

This Python file defines a simple logging class called `SimpleLogger`. The class provides a basic logging functionality that writes log messages to both the console and a file.

**Key Features:**

* Creates a logger with a specified name (default: `'my_logger'`)
* Logs messages to both the console and a file (default file: `'app.log'`)
* Log level is set to `INFO`
* Log messages are formatted with a timestamp (`%(asctime)s`) followed by the message

**Usage:**

* Create an instance of the `SimpleLogger` class, optionally specifying a logger name and log file.
* Call the instance like a function, passing a message to be logged.

**Example:**
```python
logger = SimpleLogger('my_app', 'my_app.log')
logger('This is a log message')
```
This will output:
```
2023-12-01 12:00:00,000 - This is a log message
```
to both the console and the `my_app.log` file.


---


## Class: `SimpleLogger`

No class docstring available.


### Method: `__init__`
- **Arguments**: ['self', 'name', 'log_file']
- **Returns**: None

Initializes a SimpleLogger instance.

 :param name: The name of the logger (default: 'my_logger')
 :param log_file: The file path for logging (default: 'app.log')

### Method: `__call__`
- **Arguments**: ['self', 'message']
- **Returns**: None

Logs a given message at the INFO level.

 :param message: The message to be logged. 
 :return: None



