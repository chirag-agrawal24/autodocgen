import os
import ast

try:
    from .ai_docstring_generator import generate_docstring
except ImportError:
    generate_docstring = None  # fallback if AI module not present


def parse_function(node, filename, use_ai=False, file_context=""):
    args = [arg.arg for arg in node.args.args]
    docstring = ast.get_docstring(node)

    if not docstring and use_ai and generate_docstring:
        print(f"🤖 Generating docstring for: {node.name} (AI)")
        docstring = generate_docstring(node.name, args, file_context)

    return {
        "name": node.name,
        "args": args,
        "docstring": docstring or "No docstring available.",
        "file": filename
    }


def parse_file(file_path, use_ai=False):
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast.parse(source_code, filename=file_path)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_info = parse_function(
                node,
                filename=os.path.basename(file_path),
                use_ai=use_ai,
                file_context=source_code if use_ai else ""
            )
            functions.append(func_info)

    return functions


def parse_python_files(input_dir, use_ai=False):
    all_functions = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                print(f"🔍 Parsing {full_path}")
                all_functions.extend(parse_file(full_path, use_ai=use_ai))
    return all_functions
