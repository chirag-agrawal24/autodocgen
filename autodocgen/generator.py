import os
from jinja2 import Environment, FileSystemLoader
from markdown import markdown as md_lib
from .parser import group_functions_by_file




def export_pdf(output_dir):
    try:
        from weasyprint import HTML
        index_file = os.path.join(output_dir, "index.html")
        pdf_path = os.path.join(output_dir, "documentation.pdf")
        HTML(index_file).write_pdf(pdf_path)
    except Exception as e:
        export_pdf_simple(output_dir)
    



def export_pdf_simple(output_dir):
    
    try:
        from xhtml2pdf import pisa
    except ImportError:
        print("❌ xhtml2pdf is not installed. Please install it to export PDF.")
        return
    html_file = os.path.join(output_dir, "index.html")
    pdf_file = os.path.join(output_dir, "documentation.pdf")

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    with open(pdf_file, "wb") as output:
        pisa_status = pisa.CreatePDF(html, dest=output)

    if pisa_status.err:
        print("❌ Error creating PDF")
    else:
        print(f"✅ PDF created at {pdf_file}")


def generate_readme(project_path, file_descriptions,use_ai=False):
    if use_ai:
        from .ai_docstring_generator import generate_readme_with_ai
        content = generate_readme_with_ai(project_path, file_descriptions)
    elif not content:
        content = "# 📦 Project Documentation\n\n"

        main_desc = "Auto-generated documentation for the codebase."
        content += f"{main_desc}\n\n"

        content += "## 📁 Modules\n\n"
        for path, desc in file_descriptions.items():
            rel_path = os.path.relpath(path, project_path)
            content += f"- `{rel_path}`: {desc}\n"

        content += "\n## 📄 How to Regenerate Docs\n\n"
        content += "```bash\n"
        content += "python -m yourdocgen.cli --path . --output-dir docs --fmt html --use-ai --pdf --readme\n"
        content += "```\n"

    # Write to README.md
    readme_path = os.path.join(project_path, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

def markdown_filter(text):
    return md_lib(text or "", extensions=["fenced_code"])

# def doc_url_filter(filepath, fmt="html"):
#     ext = "md" if fmt == "markdown" else "html"
#     return f"./{filepath.replace('.py', f'.{ext}')}"


def render_template(template_name, context, output_path, fmt="markdown"):
    env = Environment(loader=FileSystemLoader(searchpath=os.path.join(os.path.dirname(__file__), "templates")))
    if fmt == "html":
        env.filters["markdown"] = markdown_filter
    # env.filters["doc_url"] = lambda path: doc_url_filter(output_path, fmt)

    template = env.get_template(template_name)
    rendered = template.render(context)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)



def generate_docs(grouped, file_descriptions, output_dir, fmt="markdown"):
    ext = "md" if fmt == "markdown" else "html"
    group_template = f"grouped.{ext}.j2"
    index_template = f"index.{ext}.j2"

    # Use relative paths for both grouping and descriptions
    grouped_rel = {}
    descriptions_rel = {}

    for filepath, items in grouped.items():
        rel_path = os.path.relpath(filepath, start=os.getcwd()).replace(os.sep, "/")
        grouped_rel[rel_path] = items
        descriptions_rel[rel_path] = file_descriptions.get(filepath, "No description available.")

        output_path = os.path.join(output_dir, rel_path).replace(".py", f".{ext}")
        render_template(group_template, {
            "items": items,
            "file_path": rel_path,
            "file_description": descriptions_rel[rel_path],
        }, output_path, fmt=fmt)
        print(f"✅ Generated: {output_path}")

    index_path = os.path.join(output_dir, f"index.{ext}")
    render_template(index_template, {
        "grouped": grouped_rel,
        "file_descriptions": descriptions_rel,
    }, index_path, fmt=fmt)
    print(f"📚 Index generated: {index_path}")


