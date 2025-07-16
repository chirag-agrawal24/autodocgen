# autodocgen/runner.py

> AI summary failed.


---


## Function: `should_ignore`
- **Arguments**: ['path', 'ignore_list']
- **Returns**: None

Determines whether a file at the given path should be ignored based on the provided ignore list.

Parameters:
  path (str): The file path to check.
  ignore_list (list): A list of patterns or paths to ignore.

Returns:
  bool: True if the file should be ignored, False otherwise.


---


## Function: `run_documentation_tool`
- **Arguments**: ['args: dict', 'logger']
- **Returns**: None

Run the full documentation pipeline.

Args:
    args (dict): Dictionary of options.
    logger (callable): Logging function (default is print).

