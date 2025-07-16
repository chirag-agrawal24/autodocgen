import os
import ast
from collections import defaultdict

try:
    from .ai_docstring_generator import generate_docstring, generate_file_description_ai
except ImportError:
    generate_docstring = None
    generate_file_description_ai = None

def should_ignore(path, ignore_list):
    return any(os.path.commonpath([path, os.path.abspath(ign)]) == os.path.abspath(ign) for ign in ignore_list)

def parse_function(node, file_path, use_ai=False, context=""):
    args = []
    for arg in node.args.args:
        annotation = None
        if arg.annotation:
            try:
                annotation = ast.unparse(arg.annotation)
            except:
                pass
        args.append(f"{arg.arg}: {annotation}" if annotation else arg.arg)

    return_type = None
    if node.returns:
        try:
            return_type = ast.unparse(node.returns)
        except:
            pass

    docstring = ast.get_docstring(node)
    if not docstring and use_ai and generate_docstring:
        docstring = generate_docstring(node.name, args, context)

    return {
        "type": "function",
        "name": node.name,
        "args": args,
        "returns": return_type,
        "docstring": docstring or "No docstring available.",
        "file": file_path
    }


def parse_class(node, file_path, use_ai=False, context=""):
    methods = []
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            method = parse_function(item, file_path, use_ai, context)
            methods.append(method)

    return {
        "type": "class",
        "name": node.name,
        "docstring": ast.get_docstring(node) or "No class docstring available.",
        "methods": methods,
        "file": file_path
    }


def parse_file(file_path, use_ai=False):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            source = f.read()

    tree = ast.parse(source, filename=file_path)
    items = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            items.append(parse_function(node, file_path, use_ai, source))
        elif isinstance(node, ast.ClassDef):
            items.append(parse_class(node, file_path, use_ai, source))

    return items, source


def parse_python_files(directory, use_ai=False,ignore=[]):
    grouped = defaultdict(list)
    file_descriptions = {}

    for root, _, files in os.walk(directory):
        if should_ignore(root, ignore):
                continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                parsed, code = parse_file(path, use_ai)

                if use_ai and generate_file_description_ai:
                    summary = generate_file_description_ai(code)
                else:
                    summary = "No description available."

                file_descriptions[path] = summary
                grouped[path].extend(parsed)

    return grouped, file_descriptions

def group_functions_by_file(functions):
    grouped = defaultdict(list)
    for func in functions:
        grouped[func["file"]].append(func)
    return grouped
