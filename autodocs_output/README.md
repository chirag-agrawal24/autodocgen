# autodocgen
## Project Overview
The `autodocgen` project is an AI-powered Python code documentation generator. The project is packaged and distributed using the `setup.py` file, which specifies dependencies, entry points, and metadata. The project requires Python 3.10 or higher and can be installed using `pip`.

## Module Descriptions
### setup.py
This file is used to configure the `autodocgen` project for distribution. It specifies the project name, version, author, and contact information. The file also installs packages listed in `requirements.txt` and creates a console script `autodocgen` that calls the `main` function in `autodocgen.cli`.

### autodocgen/__init__.py
This file defines a single constant variable `GROQ_MODEL`, which is set to `"llama-3.3-70b-versatile"`. This variable appears to be the name of a specific AI model used for natural language processing or other machine learning tasks.

### autodocgen/logger.py
This file defines a class `SimpleLogger` that creates a simple logging system. The logger logs messages with an `INFO` level or higher and outputs logs to both the console and a log file (`app.log` by default).

### autodocgen/ai_docstring_generator.py
This file utilizes the Groq API to generate documentation for Python projects. It contains three main functions: `generate_file_description_ai`, `generate_docstring`, and `generate_readme_with_ai`. These functions use the Groq API to generate descriptions, docstrings, and README files for Python projects.

### autodocgen/inject_docstrings.py
This script is designed to inject docstrings into Python functions and classes in a given file. It uses the `ast` module to parse the Python code and traverses the abstract syntax tree (AST) to find functions and classes. If a function or class does not have a docstring, the script will generate one using the `generate_docstring` function.

### autodocgen/parser.py
This file is a parser for Python source code. It provides functions to extract information from Python files and directories, including function definitions, class definitions, and file descriptions. The parser can also generate summaries for files and functions using AI-powered tools.

### autodocgen/generator.py
This file provides functions for generating documentation in various formats, including HTML and PDF. It can generate README.md files, documentation files in Markdown or HTML format, and export the documentation as a PDF file.

## How to Regenerate Documentation
To regenerate documentation for the `autodocgen` project, run the following command:
```bash
python -m autodocgen.cli --path . --output-dir docs --fmt html --use-ai --pdf --readme
```
This command will generate documentation for the project in HTML format, use AI-powered documentation generation, and export the documentation as a PDF file. The resulting documentation will be written to the `docs` directory, and a README.md file will be generated.