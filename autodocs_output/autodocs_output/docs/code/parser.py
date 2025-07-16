import os
import ast
from collections import defaultdict
try:
    from autodocgen.ai_docstring_generator import generate_docstring, generate_file_description_ai
except ImportError:
    generate_docstring = None
    generate_file_description_ai = None


def parse_function(node, file_path, use_ai=False, context=''):
    """### parse_function Docstring

Parses a function from a given node in a Python file.

### Parameters

* node: The node to parse, expected to represent a function definition.
* file_path: The path to the Python file being parsed.
* use_ai: A flag indicating whether to utilize AI for parsing or not.
* context: Additional context for parsing, potentially influencing how the function is processed.

### Returns 

None"""
    args = []
    for arg in node.args.args:
        annotation = None
        if arg.annotation:
            try:
                annotation = ast.unparse(arg.annotation)
            except:
                pass
        args.append(f'{arg.arg}: {annotation}' if annotation else arg.arg)
    return_type = None
    if node.returns:
        try:
            return_type = ast.unparse(node.returns)
        except:
            pass
    docstring = ast.get_docstring(node)
    if not docstring and use_ai and generate_docstring:
        docstring = generate_docstring(node.name, args, context)
    return {'type': 'function', 'name': node.name, 'args': args, 'returns':
        return_type, 'docstring': docstring or 'No docstring available.',
        'file': file_path}


def parse_class(node, file_path, use_ai=False, context=''):
    """Parses a class from an Abstract Syntax Tree node.

 Args:
     node: The AST node representing the class.
     file_path: The path to the Python file being parsed.
     use_ai: A flag indicating whether to use AI-powered parsing.
     context: The parsing context.

 Returns:
     A parsed representation of the class."""
    methods = []
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            method = parse_function(item, file_path, use_ai, context)
            methods.append(method)
    return {'type': 'class', 'name': node.name, 'docstring': ast.
        get_docstring(node) or 'No class docstring available.', 'methods':
        methods, 'file': file_path}


def parse_file(file_path, use_ai=False):
    """### parse_file Function Docstring

Parses a Python file using the Abstract Syntax Tree (AST) module.

Extracts information such as functions, classes, docstrings, and arguments.

Args:
- file_path (str): The path to the Python file to be parsed.
- use_ai (bool): A flag indicating whether to utilize AI for parsing.

Returns:
- A structured representation of the parsed file contents."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            source = f.read()
    tree = ast.parse(source, filename=file_path)
    items = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            items.append(parse_function(node, file_path, use_ai, source))
        elif isinstance(node, ast.ClassDef):
            items.append(parse_class(node, file_path, use_ai, source))
    return items, source


def parse_python_files(directory, use_ai=False, ignore=[]):
    """### parse_python_files

Parses Python files in a specified directory, extracting functions, classes, and their corresponding docstrings and arguments.

### Args

* directory: The path to the directory containing Python files to parse.
* use_ai: A flag indicating whether to utilize AI for parsing (not specified).
* ignore: A list or pattern of files or directories to ignore during parsing (not specified).

### Returns

Not specified. 

However, here is a suggested concise, readable Python docstring:

 
Parses Python files in a directory, extracting functions, classes, and their docstrings and arguments.

Args:
    directory (str): Path to the directory containing Python files to parse.
    use_ai (bool): Flag to utilize AI for parsing.
    ignore (list or str): Files or directories to ignore during parsing.

Returns:
    None
""\""""
    grouped = defaultdict(list)
    file_descriptions = {}
    for root, _, files in os.walk(directory):
        if any(ignored in root for ignored in ignore):
            continue
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                parsed, code = parse_file(path, use_ai)
                if use_ai and generate_file_description_ai:
                    summary = generate_file_description_ai(code)
                else:
                    summary = 'No description available.'
                file_descriptions[path] = summary
                grouped[path].extend(parsed)
    return grouped, file_descriptions


def group_functions_by_file(functions):
    """Group functions by their defining file.

### Args
* functions: A list of functions to group by file

### Returns
A dictionary where keys are file names and values are lists of functions defined in each file. 

However, since you requested a concise and readable Python docstring I assume you prefer the Google style.

### group_functions_by_file
## Args
functions (list): A list of functions to group by file
## Returns
dict: A dictionary where keys are file names and values are lists of functions defined in each file"""
    grouped = defaultdict(list)
    for func in functions:
        grouped[func['file']].append(func)
    return grouped
