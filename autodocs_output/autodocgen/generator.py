import os
from jinja2 import Environment, FileSystemLoader
from markdown import markdown as md_lib
from .parser import group_functions_by_file


def export_pdf(output_dir):
    """Exports the generated content as a PDF file to the specified output directory.

Args:
    output_dir (str): The path to the directory where the PDF file will be saved.

Returns:
    None

Raises:
    FileNotFoundError: If the output directory does not exist.
    PermissionError: If the program lacks permission to write to the output directory."""
    try:
        from weasyprint import HTML
        index_file = os.path.join(output_dir, 'index.html')
        pdf_path = os.path.join(output_dir, 'documentation.pdf')
        HTML(index_file).write_pdf(pdf_path)
        return True
    except Exception as e:
        return export_pdf_simple(output_dir)


def export_pdf_simple(output_dir):
    """Exports a simple PDF file to the specified output directory.

Args:
    output_dir (str): The directory where the PDF file will be saved.

Returns:
    None

Note:
    The PDF file generated by this function is a basic representation and may not include all the features or complexities of the original content."""
    try:
        from xhtml2pdf import pisa
    except ImportError:
        print('❌ xhtml2pdf is not installed. Please install it to export PDF.')
        return False
    html_file = os.path.join(output_dir, 'index.html')
    pdf_file = os.path.join(output_dir, 'documentation.pdf')
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    with open(pdf_file, 'wb') as output:
        pisa_status = pisa.CreatePDF(html, dest=output)
    if pisa_status.err:
        print('❌ Error creating PDF')
        return False
    print(f'✅ PDF created at {pdf_file}')
    return True


def generate_readme(file_descriptions, project_path=None, output_path=None,
    use_ai=False, replace_existing=False):
    """Generates a README file based on provided file descriptions and project details.

Args:
    file_descriptions (dict): Dictionary containing file names and their descriptions.
    project_path (str): Path to the project directory.
    output_path (str): Path where the README file will be generated.
    use_ai (bool): Flag to indicate whether to use AI for summarizing content.
    replace_existing (bool): Flag to replace the existing README file if it exists.

Returns:
    None

Raises:
    FileNotFoundError: If the project path or output path does not exist.
    IOError: If an I/O error occurs while generating the README file."""
    if not project_path and not output_path:
        project_path = os.getcwd()
    if use_ai:
        from .ai_docstring_generator import generate_readme_with_ai
        content = generate_readme_with_ai(project_path, file_descriptions)
    elif not content:
        content = '# 📦 Project Documentation\n\n'
        main_desc = 'Auto-generated documentation for the codebase.'
        content += f'{main_desc}\n\n'
        content += '## 📁 Modules\n\n'
        for path, desc in file_descriptions.items():
            rel_path = os.path.relpath(path, project_path)
            content += f'- `{rel_path}`: {desc}\n'
        content += '\n## 📄 How to Regenerate Docs\n\n'
        content += '```bash\n'
        content += """python -m autodocgen run --path . --output-dir docs --fmt html --use-ai --pdf --readme
"""
        content += '```\n'
    if replace_existing or not os.path.exists(os.path.join(project_path,
        'README.md')):
        readme_path = os.path.join(project_path, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
    if output_path:
        readme_path = os.path.join(output_path, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)


def markdown_filter(text):
    """Applies Markdown formatting filters to the input text, correcting and refining it for better readability and consistency. 
Args:
    text (str): The text to be filtered and formatted.
Returns:
    str: The formatted text with applied Markdown filters."""
    return md_lib(text or '', extensions=['fenced_code'])


def render_template(template_name, context, output_path, fmt='markdown'):
    """Render a template to a file using the given context.

Args:
    template_name (str): The name of the template to render.
    context (dict): A dictionary containing variables to use in the template.
    output_path (str): The path where the rendered template will be saved.
    fmt (str): The format of the output file.

Returns:
    None

Raises:
    TypeError: If template_name, context, output_path, or fmt are of the wrong type.
    FileNotFoundError: If the template file does not exist."""
    env = Environment(loader=FileSystemLoader(searchpath=os.path.join(os.
        path.dirname(__file__), 'templates')))
    if fmt == 'html':
        env.filters['markdown'] = markdown_filter
    template = env.get_template(template_name)
    rendered = template.render(context)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)


def generate_docs(grouped, file_descriptions, output_dir, fmt='markdown',
    soucre_path=os.getcwd()):
    """Generate documentation based on the provided grouped data, file descriptions, and source path, saving it to the specified output directory in the chosen format.

Args:
    grouped (object): Grouped data used to generate documentation.
    file_descriptions (dict): Dictionary containing file descriptions.
    output_dir (str): Directory where the generated documentation will be saved.
    fmt (str): Format of the generated documentation.
    source_path (str): Path to the source files used to generate documentation.

Returns:
    None"""
    ext = 'md' if fmt == 'markdown' else 'html'
    group_template = f'grouped.{ext}.j2'
    index_template = f'index.{ext}.j2'
    grouped_rel = {}
    descriptions_rel = {}
    for filepath, items in grouped.items():
        rel_path = os.path.relpath(filepath, start=soucre_path).replace(os.
            sep, '/')
        grouped_rel[rel_path] = items
        descriptions_rel[rel_path] = file_descriptions.get(filepath,
            'No description available.')
        output_path = os.path.join(output_dir, rel_path).replace('.py',
            f'.{ext}')
        render_template(group_template, {'items': items, 'file_path':
            rel_path, 'file_description': descriptions_rel[rel_path]},
            output_path, fmt=fmt)
        print(f'Generated: {output_path}')
    index_path = os.path.join(output_dir, f'index.{ext}')
    render_template(index_template, {'grouped': grouped_rel,
        'file_descriptions': descriptions_rel}, index_path, fmt=fmt)
    print(f'Index generated: {index_path}')
