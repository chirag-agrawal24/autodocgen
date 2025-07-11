import os
import ast
import astor
import difflib

try:
    from .ai_docstring_generator import generate_docstring, generate_file_description_ai
except ImportError:
    generate_docstring = lambda name, args, context: f"{name} function description (AI unavailable)"
    generate_file_description_ai = lambda code: "No description available."


class DocstringInjector(ast.NodeTransformer):
    def __init__(self, file_context="", force=False, show_diff=False):
        self.file_context = file_context
        self.force = force
        self.show_diff = show_diff
        self.original_code = ""
        self.modified_code = ""

    def visit_FunctionDef(self, node):
        needs_doc = self.force or not ast.get_docstring(node)
        if needs_doc:
            arg_names = [arg.arg for arg in node.args.args]
            doc = generate_docstring(node.name, arg_names, self.file_context)
            doc_expr = ast.Expr(value=ast.Str(s=doc))

            # Remove old docstring if exists
            if ast.get_docstring(node):
                node.body = node.body[1:]
            node.body.insert(0, doc_expr)

        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        needs_doc = self.force or not ast.get_docstring(node)
        if needs_doc:
            doc = f"{node.name} class description."
            doc_expr = ast.Expr(value=ast.Str(s=doc))
            if ast.get_docstring(node):
                node.body = node.body[1:]
            node.body.insert(0, doc_expr)

        # Visit methods too
        self.generic_visit(node)
        return node

    def inject(self, code):
        self.original_code = code
        tree = ast.parse(code)
        self.visit(tree)
        self.modified_code = astor.to_source(tree)
        return self.modified_code

    def show_code_diff(self):
        if not self.show_diff:
            return
        print("🔍 Diff:")
        diff = difflib.unified_diff(
            self.original_code.splitlines(keepends=True),
            self.modified_code.splitlines(keepends=True),
            fromfile="Original",
            tofile="Modified"
        )
        for line in diff:
            print(line, end="")
            
def inject_into_file(filepath, dest_path=None, force=False, show_diff=False):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    file_context = generate_file_description_ai(code) if generate_file_description_ai else ""
    injector = DocstringInjector(file_context, force=force, show_diff=show_diff)
    new_code = injector.inject(code)

    if show_diff:
        injector.show_code_diff()

    dest = dest_path or filepath
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    with open(dest, "w", encoding="utf-8") as f:
        f.write(new_code)
