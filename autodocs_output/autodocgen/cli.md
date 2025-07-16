# autodocgen/cli.py

> **Python File Summary**

This Python file is the entry point for a command-line tool that generates documentation from Python source code. The tool supports two modes: CLI (Command-Line Interface) and GUI (Graphical User Interface).

### CLI Mode

The CLI mode allows users to generate documentation for a Python project by specifying the project directory, output directory, and other options. The available options are:

* `--path`: Path to the Python project directory (required)
* `--output-dir`: Directory to write the documentation (default: `docs`)
* `--fmt`: Output format (choices: `markdown`, `html`, default: `markdown`)
* `--use-ai`: Use AI to generate docstrings and file summaries
* `--pdf`: Export HTML docs to PDF
* `--readme`: Generate README.md for the project
* `--inject-docs`: Inject AI-generated docstrings into code
* `--inplace`: Modify original source files (DANGEROUS)
* `--force`: Force overwrite existing docstrings
* `--diff`: Show diff of injected docstrings
* `--ignore`: Folders to ignore (can be specified multiple times)

### GUI Mode

The GUI mode launches a graphical user interface for the tool.

### Main Functionality

The file uses the `argparse` library to parse command-line arguments and the `autodocgen` library to run the documentation tool. The main functionality of the file is to:

1. Parse command-line arguments
2. Check if the project directory exists
3. Create the output directory if it does not exist
4. Run the documentation tool with the specified options

### Example Usage

To use the tool in CLI mode, run the following command:
```bash
python autodocgen.py run --path /path/to/project --output-dir docs --fmt markdown --use-ai
```
To launch the GUI, run:
```bash
python autodocgen.py gui
```


---


## Function: `main`
- **Arguments**: []
- **Returns**: None

Generate documentation from Python source code using the autodocgen tool.

 Runs the documentation tool with provided command line arguments.

 No arguments are explicitly defined for this function, 
 it presumably uses sys.argv or argparse to parse command line arguments.

 Returns: None 

 or 

 Exit the program after running the documentation tool.

