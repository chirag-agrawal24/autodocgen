# 📘 Project Documentation Index


## [setup.py](setup.md)
  > **Summary:**

This Python file is a `setup.py` file, which is used to package and distribute a Python project. The project is called `autodocgen`, an AI-powered Python code documentation generator.

**Key Settings:**

* **Project Name and Version:** `autodocgen` version `0.1.0`
* **Author and Contact:** Chirag Agrawal, `2411chirag@gmail.com`
* **Requirements:** Installs packages listed in `requirements.txt`
* **Entry Point:** Creates a console script `autodocgen` that calls the `main` function in `autodocgen.cli`
* **Python Version:** Requires Python `3.10` or higher

**Purpose:**

This file is used to configure the `autodocgen` project for distribution, including specifying dependencies, entry points, and metadata. It allows users to install the project using `pip` and access the `autodocgen` command.

## [autodocgen/__init__.py](autodocgen/__init__.md)
  > **File Summary**

This Python file defines a single constant variable:

* `GROQ_MODEL`: a string variable set to `"llama-3.3-70b-versatile"`, which appears to be the name of a specific AI model, likely used for natural language processing or other machine learning tasks.

## [autodocgen/logger.py](autodocgen/logger.md)
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

## [autodocgen/ai_docstring_generator.py](autodocgen/ai_docstring_generator.md)
  > **Summary of Python File**

This Python file utilizes the Groq API to generate documentation for Python projects. The file contains three main functions:

1. **generate_file_description_ai**: This function takes a string of Python code and uses the Groq API to generate a description of what the code does. It sends a request to the Groq API with the code and returns the generated description.

2. **generate_docstring**: This function generates a Python docstring for a given function. It takes the function name, arguments, and an optional file context, and uses the Groq API to create a docstring.

3. **generate_readme_with_ai**: This function generates a README.md file for a Python project using the Groq API. It takes a project path, file descriptions, and an optional model as input, and returns a well-structured README.md file in markdown format.

**Key Features**

* The file uses environment variables to store the Groq API key.
* It uses the `requests` library to send HTTP requests to the Groq API.
* The `groq` library is used to interact with the Groq API.
* The file includes error handling for API request failures.

**Example Use Cases**

* Automating documentation generation for Python projects.
* Improving code readability and maintainability.
* Reducing the time and effort required to write documentation.

**Notes**

* The file assumes that the Groq API key is stored in an environment variable named `GROQ_API_KEY`.
* The `GROQ_MODEL` variable is used to specify the model used by the Groq API for generating responses.
* The file includes placeholder text for the project description and instructions on how to regenerate documentation.

## [autodocgen/inject_docstrings.py](autodocgen/inject_docstrings.md)
  > **Summary**

This Python script is designed to inject docstrings into Python functions and classes in a given file. The script uses the `ast` module to parse the Python code, and then traverses the abstract syntax tree (AST) to find functions and classes. If a function or class does not have a docstring, the script will generate one using the `generate_docstring` function.

**Key Features**

1. **Docstring Injection**: The script injects docstrings into functions and classes that do not have one.
2. **Custom Docstrings**: The script allows for custom docstrings to be provided for specific functions.
3. **File Context**: The script generates a file-level description using the `generate_file_description_ai` function.
4. **Diff Display**: The script can display the differences between the original and modified code using the `difflib` module.
5. **File Overwrite**: The script can overwrite the original file with the modified code, or write the modified code to a new file.

**Usage**

The script can be used by calling the `inject_into_file` function, which takes the following parameters:

* `filepath`: The path to the Python file to inject docstrings into.
* `dest_path`: The path to write the modified code to (optional).
* `force`: A boolean indicating whether to overwrite existing docstrings (optional).
* `show_diff`: A boolean indicating whether to display the differences between the original and modified code (optional).
* `in_memory_funcs`: A list of dictionaries containing custom docstrings for specific functions (optional).

**Example Usage**

```python
inject_into_file("path/to/file.py", show_diff=True)
```

This would inject docstrings into the functions and classes in `file.py`, display the differences between the original and modified code, and overwrite the original file with the modified code.

## [autodocgen/parser.py](autodocgen/parser.md)
  > **Summary of Python File**

This Python file is a parser for Python source code. It provides functions to extract information from Python files and directories, including:

* Function definitions with their names, arguments, return types, and docstrings
* Class definitions with their names, docstrings, and methods
* File descriptions and summaries using AI-powered tools (optional)

**Key Features**

1. **Function Parsing**: The `parse_function` function extracts information from function definitions, including:
	* Function name
	* Arguments with their annotations (if available)
	* Return type (if available)
	* Docstring (if available)
2. **Class Parsing**: The `parse_class` function extracts information from class definitions, including:
	* Class name
	* Docstring (if available)
	* Methods (parsed using `parse_function`)
3. **File Parsing**: The `parse_file` function reads a Python file, parses its contents, and extracts information about functions and classes defined in the file.
4. **Directory Parsing**: The `parse_python_files` function walks through a directory and parses all Python files found, grouping the extracted information by file.
5. **AI-Powered Summaries**: If AI-powered tools are available (imported from `ai_docstring_generator` module), the parser can generate summaries for files and functions using these tools.

**Functions and Variables**

* `should_ignore`: checks if a file or directory should be ignored based on a list of ignore paths
* `parse_function`, `parse_class`, `parse_file`, and `parse_python_files`: core parsing functions
* `group_functions_by_file`: groups functions by their file paths
* `generate_docstring` and `generate_file_description_ai`: AI-powered tools for generating docstrings and file descriptions (optional)

**Error Handling**

* The parser handles UnicodeDecodeError when reading files.
* It also catches any exceptions that occur while parsing function annotations or return types.

## [autodocgen/generator.py](autodocgen/generator.md)
  > **Summary of Python File**

This Python file appears to be part of a documentation generation tool. It provides functions for generating documentation in various formats, including HTML and PDF. Here's a breakdown of the file's contents:

### Functions

1. **`export_pdf(output_dir)`**: Exports the generated documentation as a PDF file using either `weasyprint` or `xhtml2pdf` libraries.
2. **`export_pdf_simple(output_dir)`**: A fallback function that uses `xhtml2pdf` to generate a PDF file if `weasyprint` is not available.
3. **`generate_readme(file_descriptions, project_path=None, output_path=None, use_ai=False, replace_existing=False)`**: Generates a README.md file with auto-generated documentation. It can use AI-powered documentation generation if specified.
4. **`markdown_filter(text)`**: A filter function that converts Markdown text to HTML.
5. **`render_template(template_name, context, output_path, fmt="markdown")`**: Renders a Jinja2 template with the provided context and writes the output to a file in the specified format (Markdown or HTML).
6. **`generate_docs(grouped, file_descriptions, output_dir, fmt="markdown", source_path=os.getcwd())`**: Generates documentation files in the specified format (Markdown or HTML) for the provided grouped data and file descriptions.

### Purpose

The purpose of this file is to generate documentation for a project. It can generate README.md files, documentation files in Markdown or HTML format, and export the documentation as a PDF file. The file uses various libraries, including `weasyprint`, `xhtml2pdf`, and `jinja2`, to achieve these tasks.

### Possible Use Cases

1. Automatic documentation generation for a project.
2. Generating README.md files for projects.
3. Creating documentation files in Markdown or HTML format.
4. Exporting documentation as a PDF file.

Overall, this Python file provides a set of functions for generating and exporting documentation for a project, making it a useful tool for developers and project maintainers.

## [autodocgen/runner.py](autodocgen/runner.md)
  > AI summary failed.

## [autodocgen/cli.py](autodocgen/cli.md)
  > AI summary failed.

## [autodocgen/__main__.py](autodocgen/__main__.md)
  > AI summary failed.

## [autodocgen/gui_app.py](autodocgen/gui_app.md)
  > AI summary failed.
