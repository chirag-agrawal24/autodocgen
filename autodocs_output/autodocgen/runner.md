# autodocgen/runner.py

> **Overview**

This Python file appears to be part of a documentation generation tool called `autodocgen`. It provides a function `run_documentation_tool` that runs a full documentation pipeline, which includes:

1. Parsing Python files in a specified directory
2. Generating documentation in Markdown or HTML format
3. Optionally injecting AI-generated docstrings into source files
4. Exporting the documentation as a PDF
5. Generating a README.md file

**Functionality**

The `run_documentation_tool` function takes a dictionary of options `args` and a logging function `logger` as input. It performs the following steps:

1. **Input validation**: checks if the specified path exists and creates the output directory if it doesn't exist.
2. **Parsing Python files**: uses the `parse_python_files` function to parse Python files in the specified directory, ignoring directories specified in the `ignore` list.
3. **Injecting docstrings**: if specified, injects AI-generated docstrings into source files using the `inject_into_file` function.
4. **Generating documentation**: generates documentation in the specified format (Markdown or HTML) using the `generate_docs` function.
5. **Exporting as PDF**: if specified, exports the documentation as a PDF using the `export_pdf` function.
6. **Generating README.md**: if specified, generates a README.md file using the `generate_readme` function.

**Options**

The `args` dictionary can contain the following options:

* `path`: the directory to parse Python files from
* `output`: the output directory for the generated documentation
* `fmt`: the documentation format (Markdown or HTML)
* `use_ai`: whether to use AI-generated docstrings
* `pdf`: whether to export the documentation as a PDF
* `readme`: whether to generate a README.md file
* `inject_docs`: whether to inject AI-generated docstrings into source files
* `inplace`: whether to inject docstrings into source files in-place
* `force`: whether to force injection of docstrings
* `diff`: whether to show differences between original and modified files
* `ignore`: a list of directories to ignore

**Logging**

The tool uses a `SimpleLogger` class to log messages to a file named `autodocgen.log`. The logger is used to report errors, progress, and completion of tasks.


---


## Function: `should_ignore`
- **Arguments**: ['path', 'ignore_list']
- **Returns**: None

Determines whether a file at the given path should be ignored based on the provided ignore list.

 Args:
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

