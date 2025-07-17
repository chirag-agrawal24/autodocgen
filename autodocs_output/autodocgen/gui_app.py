import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from autodocgen.parser import parse_python_files
from autodocgen.generator import generate_docs, export_pdf, generate_readme
from autodocgen.ai_docstring_generator import generate_readme_with_ai
from autodocgen.inject_docstrings import inject_into_file
from tkhtmlview import HTMLLabel


class AutoDocGUI:
    """AutoDocGUI class description."""

    def __init__(self, root):
        """Initialize the object with the root element. 

Args:
    root: The root element of the object 
Raises:
    None
Returns:
    None 
Note:
    This is a constructor method that is called when an object is instantiated from the class."""
        self.root = root
        self.root.title('🧠 AutoDocGen - GUI')
        self.project_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.ignore_paths = []
        self.functions = {}
        self.generated_docstrings = {}
        self.rejected_funcs = set()
        self.setup_ui()

    def setup_ui(self):
        """Initializes and sets up the user interface for the application, handling layout and display components."""
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(top_frame, text='📂 Project Path:').grid(row=0, column=0,
            sticky='w')
        tk.Entry(top_frame, textvariable=self.project_path, width=60).grid(row
            =0, column=1)
        tk.Button(top_frame, text='Browse', command=self.browse_project).grid(
            row=0, column=2, padx=5)
        tk.Label(top_frame, text='📁 Output Path:').grid(row=1, column=0,
            sticky='w')
        tk.Entry(top_frame, textvariable=self.output_path, width=60).grid(row
            =1, column=1)
        tk.Button(top_frame, text='Browse', command=self.browse_output).grid(
            row=1, column=2, padx=5)
        tk.Label(top_frame, text='🚫 Ignored Folders:').grid(row=2, column=0,
            sticky='nw')
        self.ignore_listbox = tk.Listbox(top_frame, height=4, width=60)
        self.ignore_listbox.grid(row=2, column=1, sticky='w')
        ignore_btns = tk.Frame(top_frame)
        ignore_btns.grid(row=2, column=2, sticky='n')
        tk.Button(ignore_btns, text='+ Add', command=self.add_ignore_folder
            ).pack(pady=2)
        tk.Button(ignore_btns, text='🗑 Clear', command=self.
            clear_ignore_folders).pack(pady=2)
        middle_frame = tk.Frame(self.root)
        middle_frame.pack(fill='x', padx=10, pady=5)
        tk.Button(middle_frame, text='🧠 Generate Docstrings', command=self.
            generate_docstrings).pack(side='left', padx=5)
        tk.Button(middle_frame, text='📄 Generate HTML', command=lambda :
            self.generate_docs('html')).pack(side='left', padx=5)
        tk.Button(middle_frame, text='📝 Generate Markdown', command=lambda :
            self.generate_docs('markdown')).pack(side='left', padx=5)
        tk.Button(middle_frame, text='📘 Generate PDF', command=self.
            generate_pdf).pack(side='left', padx=5)
        tk.Button(middle_frame, text='📖 Generate README', command=self.
            generate_readme).pack(side='left', padx=5)
        self.main_pane = tk.PanedWindow(self.root, orient='horizontal')
        self.main_pane.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree = ttk.Treeview(self.main_pane)
        self.tree.heading('#0', text='📁 Files / 🧩 Functions')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.main_pane.add(self.tree)
        self.right_frame = tk.Frame(self.main_pane)
        self.main_pane.add(self.right_frame)
        self.old_doc_label = tk.Label(self.right_frame, text='📝 Old Docstring:'
            )
        self.old_doc_label.pack(anchor='w')
        self.old_doc = tk.Text(self.right_frame, height=10, bg='#f9f9f9')
        self.old_doc.pack(fill='x')
        self.new_doc_label = tk.Label(self.right_frame, text='🤖 New Docstring:'
            )
        self.new_doc_label.pack(anchor='w')
        self.new_doc = tk.Text(self.right_frame, height=10, bg='#eaffea')
        self.new_doc.pack(fill='x')
        save_frame = tk.Frame(self.right_frame)
        save_frame.pack(fill='x', pady=5)
        tk.Button(save_frame, text='❌ Reject New Doc', command=self.
            reject_current_docstring).pack(side='left', padx=5)
        tk.Button(save_frame, text='💾 Save All Final Docstrings', command=
            self.save_final_docstrings).pack(side='right', padx=5)

    def browse_project(self):
        """Browse the current project, allowing the user to navigate and view its contents."""
        path = filedialog.askdirectory()
        if path:
            self.project_path.set(path)

    def browse_output(self):
        """Browses the output when an AI summary fails, allowing for manual review and inspection of the generated content."""
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def add_ignore_folder(self):
        """Adds the current folder to the ignore list to prevent it from being summarized in the future"""
        folder = filedialog.askdirectory()
        if folder and folder not in self.ignore_paths:
            self.ignore_paths.append(folder)
            self.ignore_listbox.insert('end', folder)

    def clear_ignore_folders(self):
        """Clears the list of ignored folders in the current repository, allowing them to be reconsidered for analysis and processing."""
        self.ignore_paths.clear()
        self.ignore_listbox.delete(0, 'end')

    def generate_docstrings(self):
        """Generates Python docstrings for classes and functions to provide documentation and readability."""
        from autodocgen.parser import parse_python_files
        from autodocgen.ai_docstring_generator import generate_docstring
        self.tree.delete(*self.tree.get_children())
        self.functions = {}
        self.generated_docstrings = {}
        self.rejected_funcs = set()
        project = self.project_path.get()
        grouped, file_descriptions = parse_python_files(project, use_ai=
            True, ignore=self.ignore_paths)
        for file_path, funcs in grouped.items():
            file_node = self.tree.insert('', 'end', text=file_path, open=False)
            for func in funcs:
                key = f"{file_path}::{func['name']}"
                self.functions[key] = func
                doc = generate_docstring(func['name'], func['args'],
                    file_descriptions.get(file_path, ''))
                self.generated_docstrings[key] = doc
                self.tree.insert(file_node, 'end', text=func['name'],
                    values=(key,))

    def on_tree_select(self, event):
        """Handles tree selection events, updating the application state accordingly based on the selected tree item and the event that triggered the selection."""
        item_id = self.tree.selection()
        if not item_id:
            return
        item = self.tree.item(item_id[0])
        func_key = item['values'][0] if item['values'] else None
        if not func_key or func_key not in self.functions:
            return
        func = self.functions[func_key]
        old_doc = func.get('docstring', '')
        new_doc = self.generated_docstrings.get(func_key, '')
        self.old_doc.delete('1.0', 'end')
        self.old_doc.insert('1.0', old_doc)
        self.new_doc.delete('1.0', 'end')
        self.new_doc.insert('1.0', new_doc)

    def reject_current_docstring(self):
        """Rejects the current document summary due to AI summary failure, allowing for further processing or manual intervention."""
        item_id = self.tree.selection()
        if not item_id:
            return
        item = self.tree.item(item_id[0])
        func_key = item['values'][0] if item['values'] else None
        if func_key:
            self.rejected_funcs.add(func_key)

    def save_final_docstrings(self):
        """Saves the final docstrings after the AI summary generation has failed, preserving the original content for further reference or manual editing."""
        for key, func in self.functions.items():
            if key in self.rejected_funcs:
                continue
            func['docstring'] = self.generated_docstrings.get(key, '')
        for filepath in set(k.split('::')[0] for k in self.functions):
            related_funcs = [{'name': k.split('::')[1], 'docstring': self.
                functions[k]['docstring']} for k in self.functions if k.
                startswith(filepath + '::') and k not in self.rejected_funcs]
            relative_path = os.path.relpath(filepath, start=self.
                project_path.get())
            output_file = os.path.join(self.output_path.get(), 'code',
                relative_path)
            inject_into_file(filepath, dest_path=output_file, force=True,
                show_diff=False, in_memory_funcs=related_funcs)
        messagebox.showinfo('Success', '✅ Docstrings injected and saved!')

    def generate_docs(self, fmt='html'):
        """Generates documentation in the specified format.

Args:
    fmt (str): The format of the documentation to be generated.

Returns:
    None

Notes:
    The generated documentation will be based on the current state of the object."""
        from autodocgen.parser import parse_python_files
        project = self.project_path.get()
        output = os.path.join(self.output_path.get(), 'project_docs')
        if not project or not output:
            messagebox.showerror('Error',
                'Please specify both project and output paths.')
            return
        os.makedirs(os.path.dirname(output), exist_ok=True)
        grouped, descriptions = parse_python_files(project, use_ai=True,
            ignore=self.ignore_paths)
        generate_docs(grouped, descriptions, output, fmt=fmt)
        messagebox.showinfo('Done', f'📘 {fmt.upper()} documentation generated!'
            )

    def generate_pdf(self):
        """Generates a PDF document based on the current object state, typically used when an AI summary fails to provide a suitable alternative."""
        output_path = os.path.join(self.output_path.get(), 'project_docs')
        output_html_path = os.path.join(output_path, 'index.html')
        if not os.path.exists(output_html_path):
            self.generate_docs('html')
        os.makedirs(output_path, exist_ok=True)
        success = export_pdf(output_path)
        if success:
            messagebox.showinfo('PDF', '📄 PDF generated!')
        else:
            messagebox.showerror('PDF Error',
                '❌ Failed to generate PDF. Please check the console for details.'
                )

    def generate_readme(self):
        """Generates a README file based on the current object's state, providing a summary of its contents and configurations, serving as a fallback when AI-powered summarization fails."""
        from autodocgen.parser import parse_python_files
        project = self.project_path.get()
        output = self.output_path.get()
        _, descriptions = parse_python_files(project, use_ai=True, ignore=
            self.ignore_paths)
        content = generate_readme_with_ai(project, descriptions)
        win = tk.Toplevel(self.root)
        win.title('📖 Edit README.md')
        win.geometry('800x600')
        text_editor = tk.Text(win, wrap='word')
        text_editor.insert('1.0', content)
        text_editor.pack(side='left', fill='both', expand=True)
        preview_frame = tk.Frame(win, width=400)
        preview_frame.pack(side='right', fill='both')
        preview_label = HTMLLabel(preview_frame, html='')
        preview_label.pack(fill='both', expand=True)

        def update_preview():
            """Updates the preview after an AI summary fails, handling any necessary corrections or adjustments to ensure accurate representation of the data."""
            import markdown
            md_text = text_editor.get('1.0', 'end')
            html = markdown.markdown(md_text, extensions=['fenced_code'])
            preview_label.set_html(html)

        def save_readme():
            """Saves a failed AI summary to a README file for future reference.
 
Args:
    summary (str): The AI summary that failed.
    filename (str): The name of the README file to save to.
 
Returns:
    None"""
            content = text_editor.get('1.0', 'end').strip()
            readme_paths = [os.path.join(project, 'README.md'), os.path.
                join(output, 'project_docs', 'README.md')]
            for path in readme_paths:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
            messagebox.showinfo('Saved',
                f'✅ README.md saved at {readme_paths[0]} and {readme_paths[1]}'
                )
            win.destroy()
        button_frame = tk.Frame(win)
        button_frame.pack(fill='x')
        tk.Button(button_frame, text='👁 Preview', command=update_preview).pack(
            side='left', padx=5, pady=5)
        tk.Button(button_frame, text='💾 Save README', command=save_readme
            ).pack(side='right', padx=5, pady=5)


def launch():
    """Launches an alternative process when AI summary fails.

Args:
    None

Returns:
    None

Raises:
    Exception: If the launch process encounters an error 

Notes:
    This function is a fallback mechanism for when AI summary generation is unsuccessful."""
    root = tk.Tk()
    app = AutoDocGUI(root)
    root.mainloop()
