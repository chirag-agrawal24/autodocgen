import os
import ast
from collections import defaultdict
try:
    from .ai_docstring_generator import generate_docstring, generate_file_description_ai
except ImportError:
    generate_docstring = None
    generate_file_description_ai = None


def should_ignore(path, ignore_list):
    """Determines whether a given file path should be ignored based on a list of ignore patterns.
 
Args:
    path (str): The file path to check.
    ignore_list (list): A list of patterns to ignore.
 
Returns:
    bool: True if the path should be ignored, False otherwise."""
    return any(os.path.commonpath([path, os.path.abspath(ign)]) == os.path.
        abspath(ign) for ign in ignore_list)


def parse_function(node, file_path, use_ai=False, context=''):
    """Parse a function node from an abstract syntax tree and generate a summary based on provided context and optionally utilizing artificial intelligence.

Args:
    node: The function node from the abstract syntax tree to parse.
    file_path: The path to the file containing the function.
    use_ai: Flag indicating whether to utilize artificial intelligence for summary generation.
    context: Contextual information to aid in summary generation.

Returns:
    A summary of the function node based on the provided context and AI usage."""
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
    """_parses a class node and returns relevant information

Args:
    node: The class node to be parsed.
    file_path: The path to the file where the class is defined.
    use_ai: Flag indicating whether to use AI for parsing.
    context: The context in which the class is being parsed.

Returns:
    Parsed class information.

Raises:
    Exception: If AI summary fails._"""
    methods = []
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            method = parse_function(item, file_path, use_ai, context)
            methods.append(method)
    return {'type': 'class', 'name': node.name, 'docstring': ast.
        get_docstring(node) or 'No class docstring available.', 'methods':
        methods, 'file': file_path}


def parse_file(file_path, use_ai=False):
    """Parse a file and return its contents, optionally using AI to generate a summary if use_ai is True.

Args:
    file_path (str): The path to the file to be parsed.
    use_ai (bool): Whether to use AI to generate a summary of the file contents. 

Returns:
    The parsed file contents, or a summary if use_ai is True."""
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
    """Parse Python files in a specified directory, optionally utilizing AI for summary generation and ignoring certain files.

Args:
    directory (str): The path to the directory containing Python files to be parsed.
    use_ai (bool): If True, use AI to generate summaries for the Python files.
    ignore (list): A list of file names or patterns to be ignored during parsing.

Returns:
    None"""
    grouped = defaultdict(list)
    file_descriptions = {}
    for root, _, files in os.walk(directory):
        if should_ignore(root, ignore):
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
    """Organizes a list of functions by their respective source files.

Args:
    functions (list): A list of function objects or their names, each associated with a source file.

Returns:
    dict: A dictionary mapping source file names to lists of functions defined within those files."""
    grouped = defaultdict(list)
    for func in functions:
        grouped[func['file']].append(func)
    return grouped
