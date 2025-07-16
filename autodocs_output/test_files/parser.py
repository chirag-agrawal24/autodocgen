import os
import ast
from collections import defaultdict
try:
    from autodocgen.ai_docstring_generator import generate_docstring, generate_file_description_ai
except ImportError:
    generate_docstring = None
    generate_file_description_ai = None


def parse_function(node, file_path, use_ai=False, context=''):
    """Parses a node from a file, utilizing AI assistance if specified.

  Args:
    node: The node to be parsed.
    file_path: The path to the file containing the node.
    use_ai: A flag indicating whether to use AI assistance during parsing.
    context: The context in which the parsing is taking place, 
             potentially influencing the parsing logic.

  Returns: 
    The parsed node."""
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
    """Parses a class from the given node and file path.

 Args:
   node: The node to parse.
   file_path: The path to the file being parsed.
   use_ai: A flag indicating whether to use AI for parsing.
   context: The context in which the parsing is taking place.

 Returns:
   The parsed class."""
    methods = []
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            method = parse_function(item, file_path, use_ai, context)
            methods.append(method)
    return {'type': 'class', 'name': node.name, 'docstring': ast.
        get_docstring(node) or 'No class docstring available.', 'methods':
        methods, 'file': file_path}


def parse_file(file_path, use_ai=False):
    """Parses a file and generates a summary, optionally leveraging AI for enhanced analysis.

 Args:
   file_path (str): The path to the file to be parsed.
   use_ai (bool): A flag indicating whether to use AI for summary generation.

 Returns:
   A summary of the file content."""
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
    """Parses Python files in a specified directory.

  directory: The path to the directory containing Python files to parse.
  use_ai: A flag indicating whether to utilize AI for parsing.
  ignore: A list or pattern of files or directories to ignore during parsing.

Returns: A parsed representation of the Python files in the directory."""
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
    """Groups a list of functions by their respective files.

 Args:
     functions: A list of functions to be grouped by file.

 Returns:
     A dictionary where keys are file names and values are lists of functions."""
    grouped = defaultdict(list)
    for func in functions:
        grouped[func['file']].append(func)
    return grouped
