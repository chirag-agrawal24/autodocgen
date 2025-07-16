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
        """Initializes the object with the given context.

 Args:
   file_context: The context for file operations.
   force: A flag to force certain operations.
   show_diff: A flag to display differences.
   in_memory_funcs: A collection of in-memory functions."""
        self.file_context = file_context
        self.force = force
        self.show_diff = show_diff
        self.in_memory_funcs = in_memory_funcs or []
        self.original_code = ''
        self.modified_code = ''

    def get_custom_docstring(self, name):
        """Returns a custom docstring for the given attribute name. 
Parameters
    self: A reference to the instance of the class
    name: The name of the attribute to retrieve the docstring for"""
        for f in self.in_memory_funcs:
            if f['name'] == name:
                return f.get('docstring')
        return None

    def visit_FunctionDef(self, node):
        """Visits a FunctionDef node in the abstract syntax tree, processing its structure and attributes. 
 
 Parameters
 -----------
 self : object
     A reference to the instance of the class
 node : object
     The FunctionDef node to be visited"""
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
        """Visits a class definition node and performs necessary actions.
 
Parameters:
self: A reference to the instance of the class
node: The class definition node to be visited"""
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
        """Injects the provided code into the current object, allowing for dynamic modification of its behavior. 
The code parameter should be a string containing valid Python code. 
Note: This method can pose a security risk if used with untrusted input, as it can evaluate arbitrary code."""
        self.original_code = code
        tree = ast.parse(code)
        self.visit(tree)
        self.modified_code = astor.to_source(tree)
        return self.modified_code

    def show_code_diff(self):
        """Displays the code difference for the AI summary failure. 
No arguments are required beyond the instance reference."""
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
    """Injects content into a file at a specified destination path.

 Args:
  filepath: The path to the file to be injected.
  dest_path: The destination path where the content will be injected.
  force: A flag to force the injection even if the file already exists.
  show_diff: A flag to display the differences between the original and injected files.
  in_memory_funcs: A list of functions to be executed in memory before injection.

 Returns:
  None"""
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
