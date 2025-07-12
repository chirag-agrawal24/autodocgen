import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from autodocgen.parser import parse_python_files
from autodocgen.generator import generate_docs, export_pdf, generate_readme
from autodocgen.inject_docstrings import inject_into_file

class AutoDocGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 AutoDocGen - GUI")

        self.project_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.functions = {}
        self.generated_docstrings = {}
        self.rejected_funcs = set()

        self.setup_ui()

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(top_frame, text="📂 Project Path:").grid(row=0, column=0, sticky="w")
        tk.Entry(top_frame, textvariable=self.project_path, width=60).grid(row=0, column=1)
        tk.Button(top_frame, text="Browse", command=self.browse_project).grid(row=0, column=2, padx=5)

        tk.Label(top_frame, text="📁 Output Path:").grid(row=1, column=0, sticky="w")
        tk.Entry(top_frame, textvariable=self.output_path, width=60).grid(row=1, column=1)
        tk.Button(top_frame, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5)

        middle_frame = tk.Frame(self.root)
        middle_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(middle_frame, text="🧠 Generate Docstrings", command=self.generate_docstrings).pack(side="left", padx=5)
        tk.Button(middle_frame, text="📄 Generate HTML", command=lambda: self.generate_docs("html")).pack(side="left", padx=5)
        tk.Button(middle_frame, text="📝 Generate Markdown", command=lambda: self.generate_docs("markdown")).pack(side="left", padx=5)
        tk.Button(middle_frame, text="📘 Generate PDF", command=self.generate_pdf).pack(side="left", padx=5)

        self.main_pane = tk.PanedWindow(self.root, orient="horizontal")
        self.main_pane.pack(fill="both", expand=True, padx=10, pady=5)

        # Left: Tree view
        self.tree = ttk.Treeview(self.main_pane)
        self.tree.heading("#0", text="📁 Files / 🧩 Functions")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.main_pane.add(self.tree)

        # Right: Split top and bottom
        self.right_frame = tk.Frame(self.main_pane)
        self.main_pane.add(self.right_frame)

        self.old_doc_label = tk.Label(self.right_frame, text="📝 Old Docstring:")
        self.old_doc_label.pack(anchor="w")
        self.old_doc = tk.Text(self.right_frame, height=10, bg="#f9f9f9")
        self.old_doc.pack(fill="x")

        self.new_doc_label = tk.Label(self.right_frame, text="🤖 New Docstring:")
        self.new_doc_label.pack(anchor="w")
        self.new_doc = tk.Text(self.right_frame, height=10, bg="#eaffea")
        self.new_doc.pack(fill="x")

        # Save actions
        save_frame = tk.Frame(self.right_frame)
        save_frame.pack(fill="x", pady=5)
        tk.Button(save_frame, text="❌ Reject This", command=self.reject_current_docstring).pack(side="left", padx=5)
        tk.Button(save_frame, text="💾 Save All Final Docstrings", command=self.save_final_docstrings).pack(side="right", padx=5)

    def browse_project(self):
        path = filedialog.askdirectory()
        if path:
            self.project_path.set(path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def generate_docstrings(self):
        from autodocgen.parser import parse_python_files
        from autodocgen.ai_docstring_generator import generate_docstring

        self.tree.delete(*self.tree.get_children())
        self.functions = {}
        self.generated_docstrings = {}
        self.rejected_funcs = set()

        project = self.project_path.get()
        grouped, file_descriptions = parse_python_files(project, use_ai=True)
        for file_path, funcs in grouped.items():
            file_node = self.tree.insert("", "end", text=file_path, open=False)
            for func in funcs:
                key = f"{file_path}::{func['name']}"
                self.functions[key] = func
                doc = generate_docstring(func['name'], func['args'], file_descriptions.get(file_path, ""))
                self.generated_docstrings[key] = doc
                self.tree.insert(file_node, "end", text=func['name'], values=(key,))

    def on_tree_select(self, event):
        item_id = self.tree.selection()
        if not item_id:
            return
        item = self.tree.item(item_id[0])
        func_key = item['values'][0] if item['values'] else None
        if not func_key or func_key not in self.functions:
            return

        func = self.functions[func_key]
        old_doc = func.get("docstring", "")
        new_doc = self.generated_docstrings.get(func_key, "")

        self.old_doc.delete("1.0", "end")
        self.old_doc.insert("1.0", old_doc)

        self.new_doc.delete("1.0", "end")
        self.new_doc.insert("1.0", new_doc)

    def reject_current_docstring(self):
        item_id = self.tree.selection()
        if not item_id:
            return
        item = self.tree.item(item_id[0])
        func_key = item['values'][0] if item['values'] else None
        if func_key:
            self.rejected_funcs.add(func_key)

    def save_final_docstrings(self):
        for key, func in self.functions.items():
            if key in self.rejected_funcs:
                continue
            func["docstring"] = self.generated_docstrings.get(key, "")

        for filepath in set(k.split("::")[0] for k in self.functions):
            related_funcs = {
                k.split("::")[1]: self.functions[k]["docstring"]
                for k in self.functions
                if k.startswith(filepath + "::") and k not in self.rejected_funcs
            }
            output_file = os.path.join(self.output_path.get(), os.path.relpath(filepath, start=self.project_path.get()))
            inject_into_file(filepath, dest_path=output_file, force=True, show_diff=False, in_memory_funcs=related_funcs)

        messagebox.showinfo("Success", "✅ Docstrings injected and saved!")

    def generate_docs(self, fmt="html"):
        from autodocgen.parser import parse_python_files
        project = self.project_path.get()
        output = self.output_path.get()
        grouped, descriptions = parse_python_files(project, use_ai=True)
        generate_docs(grouped, descriptions, output, fmt=fmt)

        messagebox.showinfo("Done", f"📘 {fmt.upper()} documentation generated!")

    def generate_pdf(self):
        self.generate_docs("html")
        export_pdf(self.output_path.get())
        messagebox.showinfo("PDF", "📄 PDF generated!")

def launch():
    root = tk.Tk()
    app = AutoDocGUI(root)
    root.mainloop()
