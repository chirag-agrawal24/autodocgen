# autodocgen/inject_docstrings.py

> **Python File Summary: Docstring Injector**

This Python file provides a tool for automatically injecting docstrings into Python code. The injector uses the Abstract Syntax Tree (AST) to parse the code, identify functions and classes, and add docstrings.

**Key Features:**

* **Docstring Generation**: The injector can generate docstrings for functions and classes using AI-powered tools (optional) or simple templates.
* **Custom Docstrings**: The injector allows providing custom docstrings for specific functions.
* **Diff Display**: The injector can display a unified diff between the original and modified code.

**Main Functionality:**

1. The `DocstringInjector` class takes in code, file context, and other options (force, show diff, in-memory functions).
2. It uses the AST to parse the code and visit functions and classes.
3. For each function or class, it checks if a docstring exists. If not, or if forced, it generates a docstring and adds it to the code.
4. The modified code is then returned or written to a file.

**Usage:**

The `inject_into_file` function is the main entry point. It takes in:

* `filepath`: The path to the Python file to inject docstrings into.
* `dest_path`: The destination path to write the modified code (optional).
* `force`: A flag to force docstring injection, even if existing docstrings are present.
* `show_diff`: A flag to display a unified diff between the original and modified code.
* `in_memory_funcs`: A list of custom functions with docstrings.

The function reads the file, creates a `DocstringInjector` instance, injects docstrings, and writes the modified code to the destination path. If `show_diff` is True, it displays the diff.


---


## Class: `DocstringInjector`

No class docstring available.


### Method: `__init__`
- **Arguments**: ['self', 'file_context', 'force', 'show_diff', 'in_memory_funcs']
- **Returns**: None

Initializes the object with the given context and settings.

    Args:
        file_context: The context of the file being processed.
        force: A flag to force certain actions.
        show_diff: A flag to display differences.
        in_memory_funcs: A collection of functions stored in memory.

    Note:
        AI-powered docstring generation is attempted but may not be available.

### Method: `get_custom_docstring`
- **Arguments**: ['self', 'name']
- **Returns**: None

Get a custom docstring for a given function or variable name.

 Parameters
 ----------
 name : str
     The name of the function or variable.

 Returns
 -------
 str
     A custom docstring for the given name. If AI is unavailable, returns a default docstring.

### Method: `visit_FunctionDef`
- **Arguments**: ['self', 'node']
- **Returns**: None

Visits a FunctionDef node and generates a docstring for it. 
 Parameters:
     node: The FunctionDef node to visit. 
 Returns:
     None

### Method: `visit_ClassDef`
- **Arguments**: ['self', 'node']
- **Returns**: None

Visits a ClassDef node and generates a docstring for it. 
No arguments are processed, only the node itself.

### Method: `inject`
- **Arguments**: ['self', 'code']
- **Returns**: None

Injects provided code into the current object, 
          generating a docstring based on the function name, 
          arguments, and context if available.

### Method: `show_code_diff`
- **Arguments**: ['self']
- **Returns**: None

Displays the code difference between the current and original versions of a file, 
 highlighting changes made to the code. 

 No arguments required.




---


## Function: `inject_into_file`
- **Arguments**: ['filepath', 'dest_path', 'force', 'show_diff', 'in_memory_funcs']
- **Returns**: None

Injects a generated docstring into an existing Python file.

 Args:
     filepath (str): Path to the Python file to inject docstring into.
     dest_path (str): Destination path to write the updated file.
     force (bool): Overwrite destination file if it already exists.
     show_diff (bool): Display a diff of changes before writing to file.
     in_memory_funcs (dict): Functions to process in-memory.

 Returns:
     None

