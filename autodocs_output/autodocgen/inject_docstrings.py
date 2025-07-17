import os
import ast
import astor
import difflib
try:
    from .ai_docstring_generator import generate_docstring, generate_file_description_ai
except ImportError:
    generate_docstring = (lambda name, args, context:
        f'{name} function description (AI unavailable)')
    generate_file_description_ai = lambda code: 'No description available.'


class DocstringInjector(ast.NodeTransformer):
    """DocstringInjector class description."""

    def __init__(self, file_context='', force=False, show_diff=False,
        in_memory_funcs=None):
        """Initialize the object with the given parameters.

Args:
    self: The instance of the class
    file_context: The context of the file being processed
    force: A flag indicating whether to force the operation
    show_diff: A flag indicating whether to show the difference
    in_memory_funcs: A list of functions to be executed in memory 

Returns:
    None 

Raises:
    None"""
        self.file_context = file_context
        self.force = force
        self.show_diff = show_diff
        self.in_memory_funcs = in_memory_funcs or []
        self.original_code = ''
        self.modified_code = ''

    def get_custom_docstring(self, name):
        """Get a custom docstring for a specified name.

Args:
    name (str): Name for which the custom docstring is to be retrieved

Returns:
    str: The custom docstring for the specified name"""
        for f in self.in_memory_funcs:
            if f['name'] == name:
                return f.get('docstring')
        return None

    def visit_FunctionDef(self, node):
        """Visits a function definition node in the abstract syntax tree, performing necessary operations on the node and its child nodes. 
Parameters
----------
self : object
    A reference to the instance of the class this method belongs to
node : FunctionDef
    The function definition node being visited"""
        existing_doc = ast.get_docstring(node)
        needs_doc = self.force or not existing_doc
        if not needs_doc:
            return self.generic_visit(node)
        custom_doc = self.get_custom_docstring(node.name)
        if not custom_doc and not self.in_memory_funcs:
            arg_names = [arg.arg for arg in node.args.args]
            custom_doc = generate_docstring(node.name, arg_names, self.
                file_context)
        if custom_doc:
            doc_expr = ast.Expr(value=ast.Str(s=custom_doc))
            if existing_doc:
                node.body = node.body[1:]
            node.body.insert(0, doc_expr)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Visits a class definition node in the abstract syntax tree. 

Args:
    self: The current instance of the class.
    node: The class definition node to be visited.

Returns:
    None"""
        existing_doc = ast.get_docstring(node)
        needs_doc = self.force or not existing_doc
        if needs_doc:
            doc = f'{node.name} class description.'
            doc_expr = ast.Expr(value=ast.Str(s=doc))
            if existing_doc:
                node.body = node.body[1:]
            node.body.insert(0, doc_expr)
        self.generic_visit(node)
        return node

    def inject(self, code):
        """Injects the provided code into the current context.

Args:
    code (str): The code to be injected.

Returns:
    None

Note:
    This function modifies the current context by injecting the given code."""
        self.original_code = code
        tree = ast.parse(code)
        self.visit(tree)
        self.modified_code = astor.to_source(tree)
        return self.modified_code

    def show_code_diff(self):
        """Displays the difference between the expected and actual code when an AI summary fails."""
        if not self.show_diff:
            return
        print('🔍 Diff:')
        diff = difflib.unified_diff(self.original_code.splitlines(keepends=
            True), self.modified_code.splitlines(keepends=True), fromfile=
            'Original', tofile='Modified')
        for line in diff:
            print(line, end='')


def inject_into_file(filepath, dest_path=None, force=False, show_diff=False,
    in_memory_funcs=None):
    """Injects data into a file at a specified destination path.

Args:
    filepath (str): The path to the file where data will be injected.
    dest_path (str): The path within the file where data will be injected.
    force (bool): If True, overwrite existing data without prompting.
    show_diff (bool): If True, display the differences between the original and modified file.
    in_memory_funcs (list): A list of in-memory functions to be applied during injection.

Returns:
    None

Raises:
    FileNotFoundError: If the file at filepath does not exist.
    PermissionError: If permission is denied to access or modify the file.
    ValueError: If the dest_path is invalid or if in_memory_funcs is not a list."""
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    file_context = generate_file_description_ai(code
        ) if generate_file_description_ai else ''
    injector = DocstringInjector(file_context=file_context, force=force,
        show_diff=show_diff, in_memory_funcs=in_memory_funcs)
    new_code = injector.inject(code)
    if show_diff:
        injector.show_code_diff()
    dest = dest_path or filepath
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(new_code)
    print(f'Docstrings injected into {dest}')
