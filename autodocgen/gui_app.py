import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import difflib

from .parser import parse_python_files
from .generator import generate_docs, generate_readme, export_pdf
from .inject_docstrings import inject_into_file

class DocGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 AutoDocGen GUI")
        self.root.geometry("1200x700")

        self.functions = []
        self.grouped = {}
        self.file_descriptions = {}
        self.path = tk.StringVar()
        self.output = tk.StringVar(value="docs")
        self.use_ai = tk.BooleanVar()
        self.force = tk.BooleanVar()
        self.hide_doc = tk.BooleanVar()
        self.show_diff = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        top = tk.Frame(self.root)
        top.pack(fill="x", pady=5)

        tk.Label(top, text="📁 Project Path:").pack(side="left")
        tk.Entry(top, textvariable=self.path, width=60).pack(side="left", padx=5)
        tk.Button(top, text="Browse", command=self.browse_path).pack(side="left")

        tk.Label(top, text="📂 Output Path:").pack(side="left", padx=10)
        tk.Entry(top, textvariable=self.output, width=30).pack(side="left", padx=5)

        opts = tk.Frame(self.root)
        opts.pack(fill="x", pady=5)
        tk.Checkbutton(opts, text="Use AI", variable=self.use_ai).pack(side="left", padx=5)
        tk.Checkbutton(opts, text="Force Overwrite", variable=self.force).pack(side="left", padx=5)
        tk.Checkbutton(opts, text="Hide Already Documented", variable=self.hide_doc, command=self.update_function_list).pack(side="left", padx=5)
        tk.Checkbutton(opts, text="Show Diff", variable=self.show_diff).pack(side="left", padx=5)

        btns = tk.Frame(self.root)
        btns.pack(fill="x", pady=5)
        tk.Button(btns, text="🔍 Scan", command=self.scan).pack(side="left", padx=5)
        tk.Button(btns, text="⚙️ Generate Docs", command=self.apply_and_generate).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.details = scrolledtext.ScrolledText(self.root, height=12)
        self.details.pack(fill="x", padx=10)

        self.edit_frame = tk.Frame(self.root)
        self.edit_frame.pack(fill="x")
        self.edit_box = scrolledtext.ScrolledText(self.edit_frame, height=8)
        self.edit_box.pack(fill="both", expand=True, padx=10, pady=5)
        tk.Button(self.edit_frame, text="💾 Save Docstring", command=self.save_docstring).pack(pady=2)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path.set(path)

    def scan(self):
        if not os.path.exists(self.path.get()):
            messagebox.showerror("Error", "Invalid path")
            return
        self.grouped, self.file_descriptions = parse_python_files(self.path.get(), use_ai=self.use_ai.get())
        self.update_function_list()

    def update_function_list(self):
        self.tree.delete(*self.tree.get_children())
        for file_path, funcs in self.grouped.items():
            rel_path = os.path.relpath(file_path, self.path.get())
            file_node = self.tree.insert("", "end", text=rel_path, open=True)
            for func in funcs:
                if self.hide_doc.get() and func["docstring"] and "No docstring" not in func["docstring"]:
                    continue
                self.tree.insert(file_node, "end", text=func["name"], values=(file_path, func["name"]))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        parent = self.tree.parent(selected[0])
        if not parent:
            return  # it's a file node
        file_path, func_name = item["values"]
        for func in self.grouped[file_path]:
            if func["name"] == func_name:
                self.current_func = func
                self.details.delete("1.0", "end")
                self.edit_box.delete("1.0", "end")

                self.details.insert("1.0", f"🔧 Function: {func['name']}\n📄 File: {func['file']}\n📥 Args: {', '.join(func['args'])}\n📜 Original:\n\n{func['docstring']}")
                self.edit_box.insert("1.0", func["docstring"])
                if self.show_diff.get() and func["docstring"] and "No docstring" not in func["docstring"]:
                    diff = self.generate_diff(func["docstring"], self.edit_box.get("1.0", "end"))
                    self.details.insert("end", "\n\n🧾 Diff:\n" + "\n".join(diff))
                break

    def generate_diff(self, old, new):
        return list(difflib.unified_diff(old.strip().splitlines(), new.strip().splitlines(), lineterm=""))

    def save_docstring(self):
        if not hasattr(self, "current_func"):
            return
        new_doc = self.edit_box.get("1.0", "end").strip()
        self.current_func["docstring"] = new_doc
        messagebox.showinfo("Saved", "Docstring updated locally.")

    def apply_and_generate(self):
        args = {
            "output": os.path.abspath(self.output.get()),
            "path": self.path.get(),
            "use_ai": self.use_ai.get(),
            "force": self.force.get(),
        }
        os.makedirs(args["output"], exist_ok=True)
        generate_docs(self.grouped, self.file_descriptions, args["output"], fmt="markdown")
        generate_docs(self.grouped, self.file_descriptions, args["output"], fmt="html")
        generate_readme(args["path"], self.file_descriptions, use_ai=args["use_ai"])
        export_pdf(args["output"])

        messagebox.showinfo("Docs Generated", "📘 Markdown, HTML, README & PDF generated.")
        self.show_doc_editors()

    def show_doc_editors(self):
        top = tk.Toplevel(self.root)
        top.title("📝 Edit Generated Documentation")
        top.geometry("1000x700")

        tabs = ttk.Notebook(top)
        tabs.pack(fill="both", expand=True)

        def load_text(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return f.read()
            except:
                return ""

        md_text = load_text(os.path.join(self.output.get(), "documentation.md"))
        html_text = load_text(os.path.join(self.output.get(), "documentation.html"))
        readme_text = load_text(os.path.join(self.path.get(), "README.md"))

        self.editor_md = self._create_tab(tabs, "Markdown", md_text)
        self.editor_html = self._create_tab(tabs, "HTML", html_text)
        self.editor_readme = self._create_tab(tabs, "README.md", readme_text)

        save_frame = tk.Frame(top)
        save_frame.pack(fill="x")

        tk.Button(save_frame, text="💾 Save Markdown", command=self.save_md).pack(side="left", padx=5)
        tk.Button(save_frame, text="💾 Save HTML", command=self.save_html).pack(side="left", padx=5)
        tk.Button(save_frame, text="💾 Save README", command=self.save_readme).pack(side="left", padx=5)
        tk.Button(save_frame, text="📄 Export PDF", command=self.export_pdf_from_html).pack(side="right", padx=5)

    def _create_tab(self, tabs, label, content):
        frame = tk.Frame(tabs)
        text_widget = scrolledtext.ScrolledText(frame, font=("Courier", 10))
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", content)
        tabs.add(frame, text=label)
        return text_widget

    def save_md(self):
        path = os.path.join(self.output.get(), "documentation.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.editor_md.get("1.0", "end").strip())
        messagebox.showinfo("Saved", "Markdown saved.")

    def save_html(self):
        path = os.path.join(self.output.get(), "documentation.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.editor_html.get("1.0", "end").strip())
        messagebox.showinfo("Saved", "HTML saved.")

    def save_readme(self):
        path = os.path.join(self.path.get(), "README.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.editor_readme.get("1.0", "end").strip())
        messagebox.showinfo("Saved", "README.md saved.")

    def export_pdf_from_html(self):
        from xhtml2pdf import pisa
        path_html = os.path.join(self.output.get(), "documentation.html")
        path_pdf = os.path.join(self.output.get(), "documentation.pdf")
        html_content = self.editor_html.get("1.0", "end")
        with open(path_pdf, "wb") as f:
            pisa.CreatePDF(html_content, dest=f)
        messagebox.showinfo("Exported", "📄 PDF created from edited HTML.")

def launch():
    root = tk.Tk()
    app = DocGenApp(root)
    root.mainloop()
