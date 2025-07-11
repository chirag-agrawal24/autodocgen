import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from autodocgen.parser import parse_python_files
from autodocgen.runner import run_documentation_tool


class DocGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📘 AutoDocGen GUI")
        self.root.geometry("1200x700")

        self.path = tk.StringVar()
        self.use_ai = tk.BooleanVar(value=True)
        self.fmt = tk.StringVar(value="html")
        self.inject = tk.BooleanVar(value=True)
        self.hide_documented = tk.BooleanVar(value=False)

        self.grouped = {}
        self.file_descriptions = {}
        self.edited_docstrings = {}

        self.setup_ui()

    def setup_ui(self):
        # 🔹 Toolbar
        toolbar = tk.Frame(self.root, pady=5)
        toolbar.pack(fill="x")

        tk.Label(toolbar, text="Project Path:").pack(side="left")
        tk.Entry(toolbar, textvariable=self.path, width=50).pack(side="left", padx=5)
        tk.Button(toolbar, text="Browse", command=self.select_folder).pack(side="left")

        tk.Checkbutton(toolbar, text="Use AI", variable=self.use_ai).pack(side="left", padx=5)
        tk.Checkbutton(toolbar, text="Inject Docstrings", variable=self.inject).pack(side="left")
        tk.OptionMenu(toolbar, self.fmt, "html", "markdown").pack(side="left", padx=5)
        tk.Checkbutton(toolbar, text="Hide Documented", variable=self.hide_documented, command=self.populate_tree).pack(side="left", padx=10)

        tk.Button(toolbar, text="Parse Files", command=self.load_functions).pack(side="left", padx=10)

        # 🔹 Treeview Panel
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(side="left", fill="y", padx=5)

        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(fill="y", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_function)

        # 🔹 Split View Panel
        editor_frame = tk.Frame(self.root)
        editor_frame.pack(side="right", fill="both", expand=True)

        self.original_label = tk.Label(editor_frame, text="Original Docstring")
        self.original_label.pack()
        self.original_text = scrolledtext.ScrolledText(editor_frame, height=10, font=("Courier", 10), bg="#f0f0f0")
        self.original_text.pack(fill="x")
        self.original_text.config(state="disabled")

        self.edit_label = tk.Label(editor_frame, text="Edited Docstring")
        self.edit_label.pack()
        self.edit_text = scrolledtext.ScrolledText(editor_frame, height=12, font=("Courier", 10))
        self.edit_text.pack(fill="both", expand=True)

        tk.Button(editor_frame, text="Apply & Generate Docs", command=self.apply_and_generate).pack(pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path.set(folder)

    def load_functions(self):
        if not os.path.exists(self.path.get()):
            messagebox.showerror("Error", "Invalid project path.")
            return

        self.edited_docstrings = {}
        self.grouped, self.file_descriptions = parse_python_files(self.path.get(), use_ai=self.use_ai.get())

        for file, funcs in self.grouped.items():
            for func in funcs:
                key = f"{file}::{func['name']}"
                self.edited_docstrings[key] = func["docstring"]

        self.populate_tree()

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        folders = {}

        for file, funcs in self.grouped.items():
            rel_path = os.path.relpath(file, self.path.get())
            folder = os.path.dirname(rel_path)

            if folder not in folders:
                folders[folder] = self.tree.insert("", "end", text=folder, open=True)

            file_id = self.tree.insert(folders[folder], "end", text=os.path.basename(file), open=True)

            for func in funcs:
                if self.hide_documented.get() and func.get("docstring") and "No docstring" not in func["docstring"]:
                    continue
                key = f"{file}::{func['name']}"
                self.tree.insert(file_id, "end", text=func["name"], values=(key,))

    def on_select_function(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        key = self.tree.item(selected, "values")
        if not key:
            return

        key = key[0]
        original = self.grouped[key.split("::")[0]]
        func_name = key.split("::")[1]
        func_data = next((f for f in original if f["name"] == func_name), None)

        if not func_data:
            return

        original_doc = func_data.get("original_docstring", func_data["docstring"])
        edited_doc = self.edited_docstrings.get(key, "")

        self.original_text.config(state="normal")
        self.original_text.delete("1.0", tk.END)
        self.original_text.insert("1.0", original_doc)
        self.original_text.config(state="disabled")

        self.edit_text.delete("1.0", tk.END)
        self.edit_text.insert("1.0", edited_doc)

    def apply_and_generate(self):
        

        selected = self.tree.focus()
        if selected:
            key = self.tree.item(selected, "values")
            if key:
                key = key[0]
                self.edited_docstrings[key] = self.edit_text.get("1.0", tk.END).strip()

        # inject updated docstrings back into grouped
        for file, funcs in self.grouped.items():
            for func in funcs:
                key = f"{file}::{func['name']}"
                if key in self.edited_docstrings:
                    func["docstring"] = self.edited_docstrings[key]

        args = {
            "path": self.path.get(),
            "output": os.path.join(self.path.get(), "docs"),
            "fmt": self.fmt.get(),
            "use_ai": self.use_ai.get(),
            "inject_docs": self.inject.get(),
            "inplace": False,
            "force": True,
            "diff": False,
            "readme": True,
            "pdf": True if self.fmt.get() == "html" else False,
        }
        md_path = os.path.join(args["output"], "documentation.md")
        html_path = os.path.join(args["output"], "documentation.html")
        readme_path = os.path.join(self.path.get(), "README.md")

        md_text = open(md_path, encoding="utf-8").read() if os.path.exists(md_path) else ""
        html_text = open(html_path, encoding="utf-8").read() if os.path.exists(html_path) else ""
        readme_text = open(readme_path, encoding="utf-8").read() if os.path.exists(readme_path) else ""

        self.show_doc_editors(md_text, html_text, readme_text)
        
        run_documentation_tool(args, logger=print)
        messagebox.showinfo("Done", "Documentation generated.")
        
    def show_doc_editors(self, md_text, html_text, readme_text):
        top = tk.Toplevel(self.root)
        top.title("📝 Edit Generated Documentation")
        top.geometry("1000x700")

        tabs = ttk.Notebook(top)
        tabs.pack(fill="both", expand=True)

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
        path = os.path.join(self.path.get(), "docs", "documentation.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.editor_md.get("1.0", "end").strip())
        messagebox.showinfo("Saved", "Markdown saved.")

    def save_html(self):
        path = os.path.join(self.path.get(), "docs", "documentation.html")
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
        path_html = os.path.join(self.path.get(), "docs", "documentation.html")
        path_pdf = os.path.join(self.path.get(), "docs", "documentation.pdf")

        html_content = self.editor_html.get("1.0", "end")

        with open(path_pdf, "wb") as f:
            pisa.CreatePDF(html_content, dest=f)

        messagebox.showinfo("Exported", "PDF created from edited HTML.")


def launch():
    root = tk.Tk()
    app = DocGenApp(root)
    root.mainloop()
